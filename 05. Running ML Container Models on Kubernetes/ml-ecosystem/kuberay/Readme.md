# KubeRay

```shell
$ helm repo add kuberay https://ray-project.github.io/kuberay-helm/
$ helm repo update
$ helm install kuberay-operator kuberay/kuberay-operator \
  --namespace kuberay-system --create-namespace
```

<br/>

```shell
$ kubectl get pods -n kuberay-system
NAME                                READY   STATUS    RESTARTS   AGE
kuberay-operator-64dd88cdd8-cvdz8   1/1     Running   0          2m4s
```

<br/>

```shell
$ kubectl create ns ai-app
$ kubectl apply -f hello-ray.yaml
```


<br/>

```shell
$ kubectl get pods -n ai-app -l ray.io/node-type=headad
NAME                         READY   STATUS    RESTARTS   AGE
hello-ray-qwvlw-head-cbvvh   1/1     Running   0          10m
```

<br/>

```shell
$ kubectl get pods -n ai-app -l ray.io/node-type=worker
NAME                                        READY   STATUS    RESTARTS   AGE
hello-ray-qwvlw-worker-group-worker-lv9ls   0/1     Pending   0          10m
hello-ray-qwvlw-worker-group-worker-nvkp8   1/1     Running   0          10m
```


<br/>

```shell
$ kubectl get rayjob hello-ray -n ai-app --watch
NAME        JOB STATUS   DEPLOYMENT STATUS   RAY CLUSTER NAME   START TIME             END TIME   AGE
hello-ray                Initializing        hello-ray-qwvlw    2026-10-01T13:26:20Z              46s
hello-ray                Initializing        hello-ray-qwvlw    2026-10-01T13:26:20Z              82s
hello-ray                Initializing        hello-ray-qwvlw    2026-10-01T13:26:20Z              94s
hello-ray                Initializing        hello-ray-qwvlw    2026-10-01T13:26:20Z              96s
hello-ray                Initializing        hello-ray-qwvlw    2026-10-01T13:26:20Z              107s
```
