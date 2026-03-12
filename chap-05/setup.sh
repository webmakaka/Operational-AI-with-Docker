#!/usr/bin/env bash
# =============================================================================
# create_chap05.sh
# Creates the complete chap-05 directory structure for:
#   PacktPublishing/Operational-AI-with-Docker
#
# Run from the repo root:
#   chmod +x create_chap05.sh && ./create_chap05.sh
# =============================================================================
set -euo pipefail

ROOT="chap-05"
echo "Creating $ROOT directory structure..."

mkdir -p "$ROOT"

# =============================================================================
# README
# =============================================================================
cat > "$ROOT/README.md" << 'MARKDOWN'
# Chapter 5: Running ML Container Models on Kubernetes

Code examples for Chapter 5 of *Operational AI with Docker* (Packt).

## Structure

```
chap-05/
├── manifests/              # Core chatbot stack (apply all at once)
│   ├── storage.yaml        # PersistentVolumeClaim for model files
│   ├── config.yaml         # ConfigMap + Secret
│   ├── dmr-deployment.yaml # Docker Model Runner Deployment + Service
│   ├── backend-deployment.yaml   # Go backend Deployment + Service
│   └── frontend-deployment.yaml  # React frontend Deployment + Service
├── scaling/
│   └── hpa.yaml            # Horizontal Pod Autoscaler for go-backend
└── ml-ecosystem/
    ├── kuberay/
    │   └── hello-ray.yaml  # Minimal RayJob to verify KubeRay
    ├── kubeflow/
    │   └── pipeline.py     # Minimal two-step Kubeflow Pipeline
    ├── kserve/
    │   └── sklearn-iris.yaml  # InferenceService example
    └── mlflow/
        ├── mlflow.yaml     # MLflow Tracking server Deployment + Service
        └── log_example.py  # Python snippet showing mlflow.log_*
```

## Prerequisites

- Docker Desktop 4.38 or later
- Kubernetes enabled via Settings → Kubernetes → kind (2 worker nodes)
- `kubectl` available (`kubectl version --client`)
- Docker Model Runner enabled in Docker Desktop with TCP port 12434
- A model pulled on the host: `docker model pull ai/smollm2:360M-Q4_K_M`

## Important: Docker Desktop kind cluster notes

When using Docker Desktop's built-in kind cluster, locally built images must
be loaded into the worker node's container runtime. The setup script handles
this automatically, but if you rebuild images you'll need to reload them:

```bash
docker save go-backend:latest | docker exec -i desktop-worker ctr -n k8s.io images import -
docker save react-frontend:latest | docker exec -i desktop-worker ctr -n k8s.io images import -
```

## Quick start

```bash
# 1. Pull the model on the host (required)
docker model pull ai/smollm2:360M-Q4_K_M

# 2. Build the application images from the Chapter 3 chatbot
docker build -t go-backend:latest ../chap-03/05-chatbot/backend/
docker build -t react-frontend:latest ../chap-03/05-chatbot/frontend/

# 3. Load images into the kind worker node
docker save go-backend:latest | docker exec -i desktop-worker ctr -n k8s.io images import -
docker save react-frontend:latest | docker exec -i desktop-worker ctr -n k8s.io images import -

# 4. Create the namespace
kubectl create namespace ai-app

# 5. Deploy everything
kubectl apply -f manifests/

# 6. Watch deployments become ready
kubectl get deployments -n ai-app --watch

# 7. Access the chatbot (run in separate terminals)
kubectl port-forward svc/react-frontend 3000:3000 -n ai-app &
kubectl port-forward svc/go-backend 8080:8080 -n ai-app &
# Open http://localhost:3000

# 8. Clean up when done
kubectl delete namespace ai-app
```

## Architecture note: DMR on Kubernetes

The `docker/model-runner` container runs the DMR HTTP server inside the
cluster on port 12434. For local development with Docker Desktop kind,
the Go backend calls the **host DMR** at `http://host.docker.internal:12434`
— the same DMR instance that serves models via `docker model run` on your Mac.

This means:
- Models are managed with `docker model pull` on the host as usual
- The in-cluster application accesses them via `host.docker.internal:12434`
- The PVC (`model-storage`) is included for future use when in-cluster model
  pulling is fully supported

For cloud Kubernetes clusters, change `LLM_URL` in `backend-deployment.yaml`
to point at the in-cluster Service: `http://docker-model-runner:12434/engines/v1`
MARKDOWN

# =============================================================================
# manifests/storage.yaml
# =============================================================================
mkdir -p "$ROOT/manifests"

cat > "$ROOT/manifests/storage.yaml" << 'YAML'
# storage.yaml — PersistentVolumeClaim for Docker Model Runner model files.
#
# On Docker Desktop kind clusters, the PVC will remain Pending until a Pod
# mounts it — this is normal behaviour (late binding). It becomes Bound
# the moment the DMR Pod starts and mounts it.
#
# Apply: kubectl apply -f storage.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: model-storage
  namespace: ai-app
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
YAML

# =============================================================================
# manifests/config.yaml
# =============================================================================
cat > "$ROOT/manifests/config.yaml" << 'YAML'
# config.yaml — ConfigMap (non-sensitive config) and Secret (credentials).
#
# MODEL_NAME must match a model already pulled on the host:
#   docker model pull ai/smollm2:360M-Q4_K_M
#
# IMPORTANT: Replace "your-api-key-here" before applying.
#
# Apply: kubectl apply -f config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: dmr-config
  namespace: ai-app
data:
  MODEL_NAME: "ai/smollm2:360M-Q4_K_M"
  DMR_HOST: "0.0.0.0"
  DMR_PORT: "12434"
---
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: ai-app
type: Opaque
stringData:
  ANTHROPIC_API_KEY: "your-api-key-here"
YAML

# =============================================================================
# manifests/dmr-deployment.yaml
# =============================================================================
cat > "$ROOT/manifests/dmr-deployment.yaml" << 'YAML'
# dmr-deployment.yaml — Docker Model Runner Deployment + Service.
#
# IMPORTANT: The containerised DMR listens on port 12434 (not 8080).
#
# On Docker Desktop kind clusters, the Go backend calls the HOST DMR at
# http://host.docker.internal:12434 rather than this in-cluster Service.
# See backend-deployment.yaml for details.
#
# Readiness probe uses /v1/models — returns 200 only when a model is loaded.
# Liveness probe uses /health — returns 200 when the HTTP server is running.
# initialDelaySeconds: 60/120 — model containers need time to load before probes fire.
#
# Apply: kubectl apply -f dmr-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-model-runner
  namespace: ai-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: docker-model-runner
  template:
    metadata:
      labels:
        app: docker-model-runner
    spec:
      containers:
        - name: model-runner
          image: docker/model-runner:latest
          ports:
            - containerPort: 12434
          envFrom:
            - configMapRef:
                name: dmr-config
          volumeMounts:
            - name: model-files
              mountPath: /models
          resources:
            requests:
              memory: "4Gi"
              cpu: "1000m"
            limits:
              memory: "8Gi"
              cpu: "4000m"
          readinessProbe:
            httpGet:
              path: /v1/models
              port: 12434
            initialDelaySeconds: 60
            periodSeconds: 10
            failureThreshold: 6
          livenessProbe:
            httpGet:
              path: /health
              port: 12434
            initialDelaySeconds: 120
            periodSeconds: 30
            failureThreshold: 3
      volumes:
        - name: model-files
          persistentVolumeClaim:
            claimName: model-storage
---
apiVersion: v1
kind: Service
metadata:
  name: docker-model-runner
  namespace: ai-app
spec:
  selector:
    app: docker-model-runner
  ports:
    - port: 12434
      targetPort: 12434
YAML

# =============================================================================
# manifests/backend-deployment.yaml
# =============================================================================
cat > "$ROOT/manifests/backend-deployment.yaml" << 'YAML'
# backend-deployment.yaml — Go backend Deployment + Service.
#
# LLM_URL points to the HOST Docker Model Runner via host.docker.internal:12434.
# This is the correct approach for Docker Desktop kind clusters — models are
# managed on the host with `docker model pull` and served from there.
#
# For cloud Kubernetes clusters, change LLM_URL to the in-cluster Service:
#   value: "http://docker-model-runner:12434/engines/v1"
#
# imagePullPolicy: Never — required for locally built images on Docker Desktop
# kind clusters. Load the image first:
#   docker save go-backend:latest | docker exec -i desktop-worker ctr -n k8s.io images import -
#
# Apply: kubectl apply -f backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: go-backend
  namespace: ai-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: go-backend
  template:
    metadata:
      labels:
        app: go-backend
    spec:
      containers:
        - name: go-backend
          image: go-backend:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 8080
          env:
            - name: LLM_URL
              value: "http://host.docker.internal:12434/engines/v1"
            - name: LLM_MODEL
              valueFrom:
                configMapKeyRef:
                  name: dmr-config
                  key: MODEL_NAME
            - name: ANTHROPIC_API_KEY
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: ANTHROPIC_API_KEY
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "500m"
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 15
---
apiVersion: v1
kind: Service
metadata:
  name: go-backend
  namespace: ai-app
spec:
  selector:
    app: go-backend
  ports:
    - port: 8080
      targetPort: 8080
YAML

# =============================================================================
# manifests/frontend-deployment.yaml
# =============================================================================
cat > "$ROOT/manifests/frontend-deployment.yaml" << 'YAML'
# frontend-deployment.yaml — React frontend Deployment + Service.
#
# The React app calls localhost:8080 for the backend (baked in at build time).
# You must run a port-forward for the go-backend Service alongside the frontend:
#   kubectl port-forward svc/go-backend 8080:8080 -n ai-app &
#   kubectl port-forward svc/react-frontend 3000:3000 -n ai-app &
#
# imagePullPolicy: Never — required for locally built images on Docker Desktop
# kind clusters. Load the image first:
#   docker save react-frontend:latest | docker exec -i desktop-worker ctr -n k8s.io images import -
#
# Apply: kubectl apply -f frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: react-frontend
  namespace: ai-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: react-frontend
  template:
    metadata:
      labels:
        app: react-frontend
    spec:
      containers:
        - name: react-frontend
          image: react-frontend:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 3000
          resources:
            requests:
              memory: "64Mi"
              cpu: "50m"
            limits:
              memory: "128Mi"
              cpu: "200m"
          readinessProbe:
            httpGet:
              path: /
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            httpGet:
              path: /
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 15
---
apiVersion: v1
kind: Service
metadata:
  name: react-frontend
  namespace: ai-app
spec:
  selector:
    app: react-frontend
  ports:
    - port: 3000
      targetPort: 3000
YAML

# =============================================================================
# scaling/hpa.yaml
# =============================================================================
mkdir -p "$ROOT/scaling"

cat > "$ROOT/scaling/hpa.yaml" << 'YAML'
# hpa.yaml — Horizontal Pod Autoscaler for the Go backend.
#
# Apply:  kubectl apply -f hpa.yaml
# Status: kubectl get hpa -n ai-app --watch
#
# Load test:
#   kubectl run load-generator \
#     --image=busybox --namespace=ai-app \
#     -- /bin/sh -c "while true; do wget -q -O- http://go-backend:8080/health; done"
#
# Cleanup: kubectl delete pod load-generator -n ai-app
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: ai-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: go-backend
  minReplicas: 1
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
YAML

# =============================================================================
# ml-ecosystem/kuberay/hello-ray.yaml
# =============================================================================
mkdir -p "$ROOT/ml-ecosystem/kuberay"

cat > "$ROOT/ml-ecosystem/kuberay/hello-ray.yaml" << 'YAML'
# hello-ray.yaml — Minimal RayJob to verify KubeRay is working.
#
# Install operator first:
#   helm repo add kuberay https://ray-project.github.io/kuberay-helm/
#   helm repo update
#   helm install kuberay-operator kuberay/kuberay-operator \
#     --namespace kuberay-system --create-namespace
#
# Apply: kubectl apply -f hello-ray.yaml
# Watch: kubectl get rayjob hello-ray -n ai-app --watch
apiVersion: ray.io/v1
kind: RayJob
metadata:
  name: hello-ray
  namespace: ai-app
spec:
  entrypoint: python -c "import ray; ray.init(); print(ray.cluster_resources())"
  rayClusterSpec:
    headGroupSpec:
      rayStartParams:
        dashboard-host: "0.0.0.0"
      template:
        spec:
          containers:
            - name: ray-head
              image: rayproject/ray:2.9.0
              resources:
                requests:
                  cpu: "1"
                  memory: "2Gi"
    workerGroupSpecs:
      - replicas: 2
        groupName: worker-group
        rayStartParams: {}
        template:
          spec:
            containers:
              - name: ray-worker
                image: rayproject/ray:2.9.0
                resources:
                  requests:
                    cpu: "1"
                    memory: "2Gi"
YAML

cat > "$ROOT/ml-ecosystem/kuberay/README.md" << 'MARKDOWN'
# KubeRay

```bash
helm repo add kuberay https://ray-project.github.io/kuberay-helm/
helm repo update
helm install kuberay-operator kuberay/kuberay-operator \
  --namespace kuberay-system --create-namespace
kubectl apply -f hello-ray.yaml
kubectl get rayjob hello-ray -n ai-app --watch
```
MARKDOWN

# =============================================================================
# ml-ecosystem/kubeflow/pipeline.py
# =============================================================================
mkdir -p "$ROOT/ml-ecosystem/kubeflow"

cat > "$ROOT/ml-ecosystem/kubeflow/pipeline.py" << 'PYTHON'
"""
pipeline.py — Minimal two-step Kubeflow Pipeline.

Install:
  export PIPELINE_VERSION=2.2.0
  kubectl apply -k \
    "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
  kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
  kubectl apply -k \
    "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"
  kubectl wait pods -l app=ml-pipeline-ui -n kubeflow --for=condition=Ready --timeout=180s
  kubectl port-forward svc/ml-pipeline-ui 8080:80 -n kubeflow

Compile: pip install kfp && python pipeline.py
Upload pipeline.yaml via http://localhost:8080
"""

from kfp import dsl


@dsl.component(base_image="python:3.11-slim")
def preprocess(data_path: str, output_path: str):
    print(f"Preprocessing {data_path} -> {output_path}")


@dsl.component(base_image="python:3.11-slim")
def train(data_path: str, model_output: str):
    print(f"Training on {data_path}, saving model to {model_output}")


@dsl.pipeline(name="simple-ml-pipeline")
def ml_pipeline(data_path: str = "/data/raw"):
    preprocess_task = preprocess(data_path=data_path, output_path="/data/processed")
    train_task = train(data_path=preprocess_task.output, model_output="/models/output")  # noqa: F841


if __name__ == "__main__":
    from kfp import compiler
    compiler.Compiler().compile(ml_pipeline, "pipeline.yaml")
    print("Compiled pipeline.yaml — upload via http://localhost:8080")
PYTHON

cat > "$ROOT/ml-ecosystem/kubeflow/README.md" << 'MARKDOWN'
# Kubeflow Pipelines

```bash
export PIPELINE_VERSION=2.2.0
kubectl apply -k \
  "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k \
  "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"
kubectl wait pods -l app=ml-pipeline-ui -n kubeflow --for=condition=Ready --timeout=180s
kubectl port-forward svc/ml-pipeline-ui 8080:80 -n kubeflow
pip install kfp && python pipeline.py
```
MARKDOWN

# =============================================================================
# ml-ecosystem/kserve/
# =============================================================================
mkdir -p "$ROOT/ml-ecosystem/kserve"

cat > "$ROOT/ml-ecosystem/kserve/sklearn-iris.yaml" << 'YAML'
# sklearn-iris.yaml — Minimal KServe InferenceService.
#
# Install:
#   kubectl apply -f \
#     https://github.com/cert-manager/cert-manager/releases/download/v1.15.0/cert-manager.yaml
#   kubectl wait --for=condition=Ready pods --all -n cert-manager --timeout=120s
#   kubectl apply -f \
#     https://github.com/kserve/kserve/releases/download/v0.13.0/kserve.yaml
#
# Apply:  kubectl apply -f sklearn-iris.yaml
# Status: kubectl get inferenceservice sklearn-iris -n ai-app --watch
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: sklearn-iris
  namespace: ai-app
spec:
  predictor:
    model:
      modelFormat:
        name: sklearn
      storageUri: "gs://kfserving-examples/models/sklearn/1.0/model"
YAML

cat > "$ROOT/ml-ecosystem/kserve/README.md" << 'MARKDOWN'
# KServe

```bash
kubectl apply -f \
  https://github.com/cert-manager/cert-manager/releases/download/v1.15.0/cert-manager.yaml
kubectl wait --for=condition=Ready pods --all -n cert-manager --timeout=120s
kubectl apply -f \
  https://github.com/kserve/kserve/releases/download/v0.13.0/kserve.yaml
kubectl apply -f sklearn-iris.yaml
kubectl get inferenceservice sklearn-iris -n ai-app --watch
```
MARKDOWN

# =============================================================================
# ml-ecosystem/mlflow/
# =============================================================================
mkdir -p "$ROOT/ml-ecosystem/mlflow"

cat > "$ROOT/ml-ecosystem/mlflow/mlflow.yaml" << 'YAML'
# mlflow.yaml — MLflow Tracking server Deployment + Service.
#
# Apply: kubectl apply -f mlflow.yaml
# UI:    kubectl port-forward svc/mlflow 5000:5000 -n ai-app
#        open http://localhost:5000
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mlflow
  namespace: ai-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mlflow
  template:
    metadata:
      labels:
        app: mlflow
    spec:
      containers:
        - name: mlflow
          image: ghcr.io/mlflow/mlflow:v2.15.0
          command:
            - mlflow
            - server
            - --host=0.0.0.0
            - --port=5000
          ports:
            - containerPort: 5000
          resources:
            requests:
              memory: "512Mi"
              cpu: "250m"
            limits:
              memory: "1Gi"
              cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: mlflow
  namespace: ai-app
spec:
  selector:
    app: mlflow
  ports:
    - port: 5000
      targetPort: 5000
YAML

cat > "$ROOT/ml-ecosystem/mlflow/log_example.py" << 'PYTHON'
"""
log_example.py — Log to the MLflow Tracking server.

Requires port-forward: kubectl port-forward svc/mlflow 5000:5000 -n ai-app
Install: pip install mlflow
"""

import mlflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("chatbot-model-fine-tune")

with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.001)
    mlflow.log_param("batch_size", 32)
    mlflow.log_param("epochs", 10)
    mlflow.log_param("model_base", "ai/smollm2:360M-Q4_K_M")
    mlflow.log_metric("eval_loss", 0.42)
    mlflow.log_metric("eval_accuracy", 0.91)
    mlflow.log_metric("tokens_per_second", 47.3)

print("Run logged. Open http://localhost:5000 to view it.")
PYTHON

cat > "$ROOT/ml-ecosystem/mlflow/README.md" << 'MARKDOWN'
# MLflow

```bash
kubectl apply -f mlflow.yaml
kubectl port-forward svc/mlflow 5000:5000 -n ai-app
pip install mlflow && python log_example.py
```
MARKDOWN

# =============================================================================
# Done
# =============================================================================
echo ""
echo "✅  Created $ROOT/ with the following structure:"
find "$ROOT" -type f | sort | sed 's/^/  /'
echo ""
echo "Next steps:"
echo "  1. docker model pull ai/smollm2:360M-Q4_K_M"
echo "  2. docker build -t go-backend:latest ../chap-03/05-chatbot/backend/"
echo "  3. docker build -t react-frontend:latest ../chap-03/05-chatbot/frontend/"
echo "  4. docker save go-backend:latest | docker exec -i desktop-worker ctr -n k8s.io images import -"
echo "  5. docker save react-frontend:latest | docker exec -i desktop-worker ctr -n k8s.io images import -"
echo "  6. kubectl create namespace ai-app"
echo "  7. kubectl apply -f $ROOT/manifests/"
echo "  8. kubectl port-forward svc/react-frontend 3000:3000 -n ai-app &"
echo "  9. kubectl port-forward svc/go-backend 8080:8080 -n ai-app &"
echo " 10. open http://localhost:3000"
