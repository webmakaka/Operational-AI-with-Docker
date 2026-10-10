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

## Docker Sandbox

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

## Docker Agent

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

## Kubernetes-native orchestration with kagent

```shell
$ cat <<EOF | kind create cluster --config=-
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- rol
```

<br/>

```shell
$ kubectl get nodes
```

<br/>

```shell
// Deploy kagent on a local cluster
$ cd 03. kagent
$ kind create cluster --config kind-cluster.yaml
$ bash install-kagent.sh
$ kubectl apply -f 03-devops-assistant/
```
