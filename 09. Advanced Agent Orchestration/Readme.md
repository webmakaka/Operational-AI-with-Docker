# Chapter 9: Advanced Agent Orchestration

В этой главе мы рассмотрим следующие основные темы:

- Безопасный запуск агентов в изолированных средах Docker
- Декларативное управление командами агентов с помощью Docker Agent
- Оркестрация на базе Kubernetes с помощью kagent
- Шаблоны развертывания в продуктивной среде и лучшие практики

К концу главы вы будете знать, как выбрать подходящий инструмент оркестрации для каждого сценария: от безопасного запуска одного агента-программиста на вашем ноутбуке до развертывания целого парка специализированных агентов, обрабатывающих задачи в кластере Kubernetes.

<br/>

```shell
$ docker sandbox --help
```

Внутри изолированной среды агент полностью автономен. Он может устанавливать системные пакеты, изменять файлы конфигурации, запускать службы и даже использовать Docker — и всё это без влияния на основную систему.

<br/>

## What you need

- Docker Desktop 4.58+ (for Sandboxes)
- Docker Agent CLI - `brew install docker/tap/docker-agent`
- For kagent stuff: kubectl, kind, Helm 3
- At least one API key (OpenAI, Anthropic, or Gemini)

<br/>

## Layout

```
sandboxes/     Docker Sandboxes commands (run interactively)
docker-agent/  Docker Agent YAML configs (run with: cagent run <file>)
kagent/        Kubernetes manifests for kagent
```

<br/>

## Quick start

```shell
// Spin up a sandbox
$ docker sandbox run claude ~/my-project
```

<br/>


```shell
// Run a cagent example
$ cd 02. docker-agent/01-pirate-assistant
$ docker agent run agents.yaml
```

<br/>

```shell
# Deploy kagent on a local cluster
$ cd 03. kagent
$ kind create cluster --config kind-cluster.yaml
$ bash install-kagent.sh
$ kubectl apply -f 03-devops-assistant/
```


<br/>

### Declarative agent teams with Docker Agent

<br/>

```shell
$ docker agent version
```
