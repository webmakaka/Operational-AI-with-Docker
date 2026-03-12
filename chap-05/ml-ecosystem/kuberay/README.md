# KubeRay

```bash
helm repo add kuberay https://ray-project.github.io/kuberay-helm/
helm repo update
helm install kuberay-operator kuberay/kuberay-operator \
  --namespace kuberay-system --create-namespace
kubectl apply -f hello-ray.yaml
kubectl get rayjob hello-ray -n ai-app --watch
```
