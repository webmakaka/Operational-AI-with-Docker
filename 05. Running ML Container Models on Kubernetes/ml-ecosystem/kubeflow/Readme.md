# Kubeflow Pipelines

```shell
$ export PIPELINE_VERSION=2.2.0

$ kubectl apply -k \
  "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"

$ kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io

$ kubectl apply -k \
  "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"

$ kubectl wait pods -l app=ml-pipeline-ui -n kubeflow --for=condition=Ready --timeout=180s
```

<br/>

```shell
$ kubectl port-forward svc/ml-pipeline-ui 8080:80 -n kubeflow
```

<br/>

```shell
$ pip install kfp && python pipeline.py
```
