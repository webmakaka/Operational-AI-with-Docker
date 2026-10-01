# KServe

```shell
$ kubectl apply -f \
  https://github.com/cert-manager/cert-manager/releases/download/v1.15.0/cert-manager.yaml

$ kubectl wait --for=condition=Ready pods --all -n cert-manager --timeout=120s

$ kubectl apply -f \
  https://github.com/kserve/kserve/releases/download/v0.13.0/kserve.yaml
```

<br/>

```shell
$ kubectl create ns ai-app
$ kubectl apply -f sklearn-iris.yaml

$ kubectl get inferenceservice sklearn-iris -n ai-app --watch
```
