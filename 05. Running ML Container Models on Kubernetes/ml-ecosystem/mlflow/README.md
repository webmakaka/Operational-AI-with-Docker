# MLflow

```bash
kubectl apply -f mlflow.yaml
kubectl port-forward svc/mlflow 5000:5000 -n ai-app
pip install mlflow && python log_example.py
```
