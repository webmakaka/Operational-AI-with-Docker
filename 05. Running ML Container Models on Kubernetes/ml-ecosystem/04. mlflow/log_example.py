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
