# MLflow

<br/>

```bash
$ kubectl create ns ai-app
```

<br/>

```bash
$ kubectl apply -f mlflow.yaml
```

<br/>

```bash
$ kubectl port-forward svc/mlflow 5000:5000 -n ai-app
```

<br/>

http://localhost:5000/

<br/>

```bash
$ pip install mlflow && python log_example.py
```
