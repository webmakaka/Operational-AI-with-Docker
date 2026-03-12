# KServe — production model serving

KServe adds an `InferenceService` custom resource that handles:
- Pulling and serving models from S3, GCS, or other artifact stores
- Scale-to-zero to reduce GPU costs during off-peak hours
- Canary deployments for gradual model rollouts
- A standardised prediction endpoint for multiple model types

## Install KServe

```bash
# 1. Install cert-manager (required by KServe webhooks)
kubectl apply -f \
  https://github.com/cert-manager/cert-manager/releases/download/v1.15.0/cert-manager.yaml

kubectl wait --for=condition=Ready pods --all \
  -n cert-manager --timeout=120s

# 2. Install KServe
kubectl apply -f \
  https://github.com/kserve/kserve/releases/download/v0.13.0/kserve.yaml
```

## Deploy the example InferenceService

```bash
kubectl apply -f sklearn-iris.yaml

# Watch it become ready
kubectl get inferenceservice sklearn-iris -n ai-app --watch
```

## Supported model formats

`sklearn`, `tensorflow`, `pytorch`, `xgboost`, `onnx`, and others are
built in. Change `modelFormat.name` and `storageUri` to serve a
different model type.

## When to use KServe

Reach for KServe when you need to:
- Serve multiple model types from a single consistent endpoint
- Cut GPU costs with scale-to-zero during off-peak hours
- Gradually shift traffic between model versions with canary deployments

For a single-model inference service like the chatbot in this chapter,
Docker Model Runner is the right choice.
