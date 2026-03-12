"""
log_example.py — Logging parameters, metrics, and artefacts to the MLflow
Tracking server running on your kind cluster.

Run this from inside a Pod in the ai-app namespace (or any Pod that can
reach the mlflow Service). From outside the cluster during development,
run: kubectl port-forward svc/mlflow 5000:5000 -n ai-app
and change the tracking URI to http://localhost:5000.

Install: pip install mlflow
"""

import mlflow

# Point the MLflow client at the in-cluster Tracking server.
# The Service name "mlflow" resolves via Kubernetes internal DNS.
mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("chatbot-model-fine-tune")

with mlflow.start_run():
    # Log hyperparameters — immutable for this run
    mlflow.log_param("learning_rate", 0.001)
    mlflow.log_param("batch_size", 32)
    mlflow.log_param("epochs", 10)
    mlflow.log_param("model_base", "ai/llama3.2:3B-Q4_K_M")

    # --- your training loop runs here ---
    # e.g. for epoch in range(10): train_step(); eval_step()

    # Log final evaluation metrics
    mlflow.log_metric("eval_loss", 0.42)
    mlflow.log_metric("eval_accuracy", 0.91)
    mlflow.log_metric("tokens_per_second", 47.3)

    # Save the trained model artefact alongside the run's metadata
    # mlflow.log_artifact("model.pkl")
    # mlflow.log_artifact("tokenizer/")

print("Run logged. Open http://localhost:5000 to see it in the MLflow UI.")
print("(Ensure port-forward is running: kubectl port-forward svc/mlflow 5000:5000 -n ai-app)")
