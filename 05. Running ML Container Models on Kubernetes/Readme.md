# Chapter 5: Running ML Container Models on Kubernetes

<br/>

```bash
$ kind create cluster --name platform-dev --image kindest/node:v1.37.0 --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
    extraPortMappings:
      - containerPort: 80
        hostPort: 8080
      - containerPort: 443
        hostPort: 8443
EOF
```

<br/>

## Quick start

```bash
// 1. Pull the model on the host (required)
$ docker model pull ai/smollm2:360M-Q4_K_M

// 2. Build the application images from the Chapter 3 chatbot
$ cd Operational-AI-with-Docker/03. Model Serving with Docker Model Runner
$ docker build -t go-backend:latest 05-chatbot/backend/
$ docker build -t react-frontend:latest 05-chatbot/frontend/

// 3. Load images into the kind
$ kind --name platform-dev load docker-image go-backend:latest
$ kind --name platform-dev load docker-image react-frontend:latest

// 4. Create the namespace
$ kubectl create namespace ai-app

// 5. Deploy everything
$ kubectl apply -f manifests/
```

<br/>

```shell
// 6. Watch deployments become ready
$ kubectl get deployments -n ai-app --watch
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
docker-model-runner   1/1     1            1           2m27s
go-backend            1/1     1            1           2m27s
react-frontend        1/1     1            1           2m27s
```

<br/>

```shell
// 7. Access the chatbot (run in separate terminals)
$ kubectl port-forward svc/react-frontend 3000:3000 -n ai-app &
$ kubectl port-forward svc/go-backend 8080:8080 -n ai-app &
```

<br/>

// Open http://localhost:3000

<br/>

```shell
// 8. Clean up when done
$ kubectl delete namespace ai-app
```

<br/>

### Delete Kind cluster

```
$ kind delete cluster --name platform-dev
```

<br/>

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

<br/>

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
