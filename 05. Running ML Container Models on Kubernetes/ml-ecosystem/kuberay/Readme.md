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
$ kubectl apply -f hello-ray.yaml
$ kubectl get rayjob hello-ray -n ai-app --watch
```
