"""
pipeline.py — Minimal two-step Kubeflow Pipeline.

Each @dsl.component function runs as its own container in Kubernetes.
The pipeline wires them together: preprocess runs first, train receives
its output. The compiler converts this Python definition to a YAML file
you upload to the Kubeflow Pipelines UI.

Prerequisites — install Kubeflow Pipelines on your kind cluster:

  export PIPELINE_VERSION=2.2.0

  kubectl apply -k \
    "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"

  kubectl wait --for condition=established \
    --timeout=60s crd/applications.app.k8s.io

  kubectl apply -k \
    "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"

  # Wait for the UI to become ready (2-3 minutes)
  kubectl wait pods -l app=ml-pipeline-ui \
    -n kubeflow --for=condition=Ready --timeout=180s

  # Open the UI
  kubectl port-forward svc/ml-pipeline-ui 8080:80 -n kubeflow
  # Navigate to http://localhost:8080

Compile and run:

  pip install kfp
  python pipeline.py       # produces pipeline.yaml
  # Upload pipeline.yaml via the Kubeflow UI, create an experiment, trigger a run
"""

from kfp import dsl


@dsl.component(base_image="python:3.11-slim")
def preprocess(data_path: str, output_path: str):
    """Step 1 — clean and split the dataset."""
    # In a real pipeline, load data_path, clean it, and write to output_path
    print(f"Preprocessing {data_path} -> {output_path}")


@dsl.component(base_image="python:3.11-slim")
def train(data_path: str, model_output: str):
    """Step 2 — run the training loop."""
    # In a real pipeline, load processed data and run model training
    print(f"Training on {data_path}, saving model to {model_output}")


@dsl.pipeline(name="simple-ml-pipeline")
def ml_pipeline(data_path: str = "/data/raw"):
    """Two-step pipeline: preprocess then train."""
    preprocess_task = preprocess(
        data_path=data_path,
        output_path="/data/processed",
    )
    train_task = train(                          # noqa: F841
        data_path=preprocess_task.output,
        model_output="/models/output",
    )


if __name__ == "__main__":
    from kfp import compiler
    compiler.Compiler().compile(ml_pipeline, "pipeline.yaml")
    print("Compiled pipeline.yaml — upload this file to the Kubeflow UI.")
