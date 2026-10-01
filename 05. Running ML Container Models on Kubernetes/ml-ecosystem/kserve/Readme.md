# KServe

```shell
$ kubectl apply -f \
  https://github.com/cert-manager/cert-manager/releases/download/v1.15.0/cert-manager.yaml

$ kubectl wait --for=condition=Ready pods --all -n cert-manager --timeout=120s

$ kubectl apply -f \
  https://github.com/kserve/kserve/releases/download/v0.13.0/kserve.yaml

$ kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.13.0/kserve-cluster-resources.yaml
```

<br/>

```shell
$ kubectl get pods -n cert-manager
NAME                                       READY   STATUS    RESTARTS   AGE
cert-manager-5b49d794c9-qb4gx              1/1     Running   0          9m14s
cert-manager-cainjector-7c4f67d58b-kh99f   1/1     Running   0          9m14s
cert-manager-webhook-7f95656c46-cnmn9      1/1     Running   0          9m14s
```


<br/>

```shell
$ kubectl get pods -n kserve
NAME                                         READY   STATUS         RESTARTS   AGE
kserve-controller-manager-66f7fd46fd-86hh9   1/2     ErrImagePull   0          2m4s
```

<br/>

```shell
$ kubectl edit deployment kserve-controller-manager -n kserve

***
quay.io/brancz/kube-rbac-proxy:v0.13.1
***
```

<br/>

```shell
$ kubectl get pods -n kserve
NAME                                         READY   STATUS    RESTARTS   AGE
kserve-controller-manager-785978bd74-xkr94   2/2     Running   0          97s
```

<br/>

```shell
$ kubectl create ns ai-app
$ kubectl apply -f sklearn-iris.yaml
```

<br/>

```shell
$ kubectl get pods -n ai-app
NAME                                     READY   STATUS    RESTARTS   AGE
sklearn-iris-predictor-bbcf57c48-xg6ps   1/1     Running   0          88s
```

<br/>

```shell
$ kubectl get inferenceservice sklearn-iris -n ai-app
NAME           URL                                      READY   PREV   LATEST   PREVROLLEDOUTREVISION   LATESTREADYREVISION   AGE
sklearn-iris   http://sklearn-iris-ai-app.example.com   True                                                                  107s                                                                     110s
```
