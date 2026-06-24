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
