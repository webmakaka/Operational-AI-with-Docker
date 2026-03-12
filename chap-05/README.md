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
