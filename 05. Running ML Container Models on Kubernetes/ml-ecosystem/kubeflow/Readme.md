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
$ kubectl get pods -n kubeflow
NAME                                               READY   STATUS              RESTARTS      AGE
cache-deployer-deployment-6f78876457-2fkdc         1/1     Running             0             3m
cache-server-547c5f95bb-2klmd                      0/1     ContainerCreating   0             3m
controller-manager-5445c75dc8-x5fs7                1/1     Running             0             3m
metadata-envoy-deployment-644b4c869f-mvk62         1/1     Running             0             3m
metadata-grpc-deployment-85dccd995d-gc6xx          0/1     CrashLoopBackOff    3 (25s ago)   3m
metadata-writer-5c5bcd59cc-mqqts                   1/1     Running             0             3m
minio-5dfdb78874-pgs2g                             0/1     ContainerCreating   0             3m
ml-pipeline-85c899867-4mqbp                        0/1     ContainerCreating   0             2m59s
ml-pipeline-persistenceagent-78f5758c4-5gjb8       0/1     ContainerCreating   0             2m59s
ml-pipeline-scheduledworkflow-7b8dcf94b7-k756l     0/1     ContainerCreating   0             2m59s
ml-pipeline-ui-7bfdcbb488-mdb5x                    0/1     ContainerCreating   0             2m59s
ml-pipeline-viewer-crd-6cc848f4b9-56wjg            0/1     ContainerCreating   0             2m59s
ml-pipeline-visualizationserver-859cdf6f9d-vh7d8   0/1     ContainerCreating   0             2m59s
mysql-7b455cfcdb-9f7f7                             0/1     ContainerCreating   0             2m59s
proxy-agent-7d97b97df-9c5bq                        0/1     ContainerCreating   0             2m58s
workflow-controller-6d9d796b5f-5f6m7               0/1     ContainerCreating   0             2m58s
```

<br/>

```shell
$ kubectl port-forward svc/ml-pipeline-ui 8080:80 -n kubeflow
```

<br/>

```shell
$ pip install kfp && python pipeline.py
```
