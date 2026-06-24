#!/bin/bash
# Install kagent on a kind cluster
set -e

echo "Creating kind cluster..."
kind create cluster --config kind-cluster.yaml 2>/dev/null || echo "Cluster already exists"

echo "Adding kagent Helm repo..."
helm repo add kagent https://kagent-ai.github.io/kagent/
helm repo update

echo "Installing kagent..."
helm install kagent kagent/kagent \
  --set apiKey="${OPENAI_API_KEY}" \
  --namespace kagent \
  --create-namespace

echo "Waiting for controller..."
kubectl wait --for=condition=ready pod -l app=kagent -n kagent --timeout=120s

echo "Done. Verify with: kubectl get pods -n kagent"
