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
$ kubectl get pods -n ai-app
NAME                                        READY   STATUS      RESTARTS   AGE
hello-ray-6j5xw                             0/1     Completed   0          2m6s
hello-ray-m7h29-head-96mx9                  1/1     Running     0          2m28s
hello-ray-m7h29-worker-group-worker-t8vp8   1/1     Running     0          2m28s
hello-ray-m7h29-worker-group-worker-zpwq8   1/1     Running     0          2m28s
```

<br/>

```shell
$ kubectl get rayjob hello-ray -n ai-app --watch
NAME        JOB STATUS   DEPLOYMENT STATUS   RAY CLUSTER NAME   START TIME             END TIME               AGE
hello-ray   SUCCEEDED    Complete            hello-ray-m7h29    2026-10-01T13:41:14Z   2026-10-01T13:41:47Z   52s
```

<br/>

```shell
$ kubectl logs -n ai-app hello-ray-6j5xw
2026-10-01 06:41:41,329	INFO cli.py:36 -- Job submission server address: http://hello-ray-m7h29-head-svc.ai-app.svc.cluster.local:8265
2026-10-01 06:41:41,844	SUCC cli.py:60 -- --------------------------------------------
2026-10-01 06:41:41,844	SUCC cli.py:61 -- Job 'hello-ray-sfqcr' submitted successfully
2026-10-01 06:41:41,844	SUCC cli.py:62 -- --------------------------------------------
2026-10-01 06:41:41,844	INFO cli.py:285 -- Next steps
2026-10-01 06:41:41,844	INFO cli.py:286 -- Query the logs of the job:
2026-10-01 06:41:41,844	INFO cli.py:288 -- ray job logs hello-ray-sfqcr
2026-10-01 06:41:41,845	INFO cli.py:290 -- Query the status of the job:
2026-10-01 06:41:41,845	INFO cli.py:292 -- ray job status hello-ray-sfqcr
2026-10-01 06:41:41,845	INFO cli.py:294 -- Request the job to be stopped:
2026-10-01 06:41:41,845	INFO cli.py:296 -- ray job stop hello-ray-sfqcr
2026-10-01 06:41:43,658	INFO cli.py:36 -- Job submission server address: http://hello-ray-m7h29-head-svc.ai-app.svc.cluster.local:8265
2026-10-01 06:41:43,111	INFO worker.py:1405 -- Using address 10.244.0.8:6379 set in the environment variable RAY_ADDRESS
2026-10-01 06:41:43,111	INFO worker.py:1540 -- Connecting to existing Ray cluster at address: 10.244.0.8:6379...
2026-10-01 06:41:43,117	INFO worker.py:1715 -- Connected to Ray cluster. View the dashboard at http://10.244.0.8:8265 
{'memory': 32930265091.0, 'object_store_memory': 14813630052.0, 'node:10.244.0.10': 1.0, 'CPU': 3.0, 'node:10.244.0.9': 1.0, 'node:__internal_head__': 1.0, 'node:10.244.0.8': 1.0}
2026-10-01 06:41:44,765	SUCC cli.py:60 -- -------------------------------
2026-10-01 06:41:44,766	SUCC cli.py:61 -- Job 'hello-ray-sfqcr' succeeded
2026-10-01 06:41:44,766	SUCC cli.py:62 -- -------------------------------
```

<br/>

```
$ kubectl delete ns ai-app
$ kubectl delete ns kuberay-system
```
