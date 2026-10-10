# Chapter 9: Advanced Agent Orchestration

В этой главе мы рассмотрим следующие основные темы:

- Безопасный запуск агентов в изолированных средах Docker
- Декларативное управление командами агентов с помощью Docker Agent
- Оркестрация на базе Kubernetes с помощью kagent
- Шаблоны развертывания в продуктивной среде и лучшие практики

К концу главы вы будете знать, как выбрать подходящий инструмент оркестрации для каждого сценария: от безопасного запуска одного агента-программиста на вашем ноутбуке до развертывания целого парка специализированных агентов, обрабатывающих задачи в кластере Kubernetes.

<br/>

## Layout

```
01. sandboxes/     Docker Sandboxes commands (run interactively)
02. docker-agent/  Docker Agent YAML configs (run with: cagent run <file>)
03. kagent/        Kubernetes manifests for kagent
```

<br/>

## 01. Docker Sandbox

<br/>

```shell
$ docker sandbox --help
```

Внутри изолированной среды агент полностью автономен. Он может устанавливать системные пакеты, изменять файлы конфигурации, запускать службы и даже использовать Docker — и всё это без влияния на основную систему.

<br/>

```shell
// Spin up a sandbox
$ docker sandbox run claude ~/my-project
```

<br/>

## 02. Docker Agent

<br/>

https://github.com/docker/docker-agent/releases

<br/>

```shell
$ cd ~/tmp
$ wget https://github.com/docker/docker-agent/releases/download/v1.150.0/docker-agent-linux-amd64
$ mkdir -p ~/.docker/cli-plugins
$ mv docker-agent-linux-amd64 ~/.docker/cli-plugins/
$ mv ~/.docker/cli-plugins/docker-agent-linux-amd64 ~/.docker/cli-plugins/docker-agent
$ chmod +x ~/.docker/cli-plugins/docker-agent
```

<br/>

```shell
$ docker agent version

Welcome to docker agent! 🚀

For any feedback, please visit: https://docker.qualtrics.com/jfe/form/SV_cNsCIg92nQemlfw

We collect anonymous usage data to help improve docker agent. To disable:
  - Set environment variable: TELEMETRY_ENABLED=false

docker agent version v1.150.0
Commit: 5277e7842058fc3fbb9943a6e88bc05a1c8e6fe2
```


<br/>

```shell
// Option 1: OpenAI
$ export OPENAI_API_KEY=sk-your-key-here

// Option 2: Anthropic
$ export ANTHROPIC_API_KEY=sk-ant-your-key-here

// Option 3: Google Gemini
$ export GEMINI_API_KEY=your-key-here

// Option 4: Docker Model Runner (free, local)
// No API key needed - uses your local DMR instance
```

<br/>

```shell
// Run a cagent example
$ cd 02. docker-agent/01-pirate-assistant
$ docker agent run agents.yaml
```





<br/>

## 03. Kubernetes-native orchestration with kagent

<br/>

```shell
// Deploy kagent on a local cluster
$ cd 03. kagent
$ kind create cluster --config kind-cluster.yaml
$ bash install-kagent.sh
```

<br/>

```shell
$ kagent version
```

<br/>

```shell
$ kubectl apply -f 03-devops-assistant/
```

<br/>

```shell
$ kagent invoke -t "What pods are running in the kagent namespace?" --agent k8s-agent
```

<br/>


```shell
$ kubectl -n kagent port-forward service/kagent-ui 8080:8080
```

<br/>

Then open http://localhost:8080 in your browser.

<br/>

### Building multi-agent architectures

<br/>

```shell
$ kubectl apply -f 02-ops-team/
$ kagent get agent | grep -E "ops-coordinator|log-analyzer|metrics-checker"
$ kagent invoke -t "Check for any pod errors in the kagent namespace" --agent ops-coordinator
```

<br/>

### Deploying MCP servers with kmcp

<br/>

```shell
$ curl -fsSL https://raw.githubusercontent.com/kagent-dev/kmcp/refs/heads/main/scripts/get-kmcp.sh | bash
```

<br/>

```shell
$ kmcp deploy package \
    --deployment-name my-mcp-server \
    --manager npx \
    --args @modelcontextprotocol/server-everything \
    --namespace kagent
```

or

```yaml
apiVersion: kagent.dev/v1alpha
kind: MCPServer
metadata:
  name: mcp-website-fetcher
  namespace: kagent
spec:
  deployment:
    args:
      - mcp-server-fetch
    cmd: uvx
    port: 3000
    stdioTransport: {}
  transportType: stdio
```

<br/>

```
// For secrets management, use Kubernetes Secrets:
$ kubectl create secret generic mcp-credentials \
    --from-literal=github-token=ghp_your_token \
    --from-literal=slack-token=xoxb-your-token \
    -n kagent
```

<br/>

### Autoscaling and resource optimization


```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: log-analyzer-hpa
  namespace: kagent
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: log-analyzer
  minReplicas: 1
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

<br/>

```
$ kubectl get hpa -n kagent
```

<br/>

```shell
apiVersion: kagent.dev/v1alpha2
kind: Agent
metadata:
  name: log-analyzer
  namespace: kagent
spec:
  description: "Analyzes Kubernetes logs for issues"
  type: Declarative
  declarative:
    modelConfig: default-model-config
    systemMessage: |
      Analyze Kubernetes pod logs to identify errors,
      warnings, and anomalies. Report findings concisely.
    deployment:
      resources:
        requests:
          cpu: "500m"
          memory: "512Mi"
        limits:
          cpu: "2"
          memory: "2Gi"
    tools:
      - type: Mcpserver
        mcpServer:
          name: kagent-tool-server
          kind: RemoteMCPServer
          toolNames:
            - k8s_get_pod_logs
            - k8s_get_events
```

<br/>

### Observability with Prometheus and tracing


<br/>

```shell
$ helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
$ helm repo update
```

<br/>

```shell
$ helm install monitoring prometheus-community/kube-prometheus-stack\
--namespace monitoring\
--create-namespace
```

<br/>

```shell
$ kubectl get pods -n monitoring
```

<br/>

```shell
$ kubectl --namespace monitoring get secrets monitoring-grafana \
-o jsonpath="{.data.admin-password}" | base64 -d; echo
```

<br/>

```shell
$ kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring
```

Open http://localhost:3000

<br/>

For distributed tracing across multi-agent workflows, deploy Jaeger:

<br/>

```shell
$ cat << 'EOF' > jaeger.yaml
provisionDataStore:
  cassandra: false
allInOne:
  enabled: true
storage:
  type: memory
agent:
  enabled: false
collector:
  enabled: false
query:
  enabled: false
EOF
```

<br/>

```shell
$ helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
$ helm repo update
```

<br/>

```shell
$ helm upgrade --install jaeger jaegertracing/jaeger \
--namespace jaeger \
--create-namespace \
--values jaeger.yaml \
--version 4.4.7
```


<br/>

Access the Jaeger UI:

```shell
$ export POD_NAME=$(kubectl get pods --namespace jaeger \
-l "app.kubernetes.io/instance=jaeger,app.kubernetes.io/component=all-in-one" \
-o jsonpath="{.items[0].metadata.name}")

$ kubectl port-forward --namespace jaeger $POD_NAME 16686:16686 &
```

<br/>

Open http://localhost:16686

<br/>

Generate tracing data by invoking an agent:

```shell
$ kagent invoke -t "What pods are running in the kagent namespace?" --agent k8s-agent
```

<br/>

### Network policies for security isolation

<br/>

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: agent-isolation
  namespace: kagent
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: k8s-agent
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: kagent
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: kagent
```

<br/>

```
$ kubectl get pods -n kagent --show-labels | grep k8s-agent
```

<br/>

## Выбор подходящего инструмента оркестрации


| Сценарий | Инструмент | Почему |
| :--- | :--- | :--- |
| Безопасный запуск агента для программирования на локальном компьютере | Песочницы Docker | Изоляция с помощью микро-ВМ, временное окружение |
| Создание команды из трёх агентов для проекта | Docker Agent | Один YAML-файл, без кода для настройки инфраструктуры |
| Обмен конфигурациями агентов с командой | Docker Agent (push/pull) | OCI-артефакты через Docker Hub |
| Создание прототипов рабочих процессов агентов | Docker Agent | Самые быстрые циклы итерации |
| Масштабирование агентов в рабочей среде | kagent | Автомасштабирование, самовосстановление и наблюдаемость |
| Развёртывание агентов на нескольких узлах | kagent | Планирование и сетевое взаимодействие в Kubernetes |
| Требования к корпоративному соответствию стандартам | kagent | Управление доступом на основе ролей (RBAC), сетевые политики и аудит |
