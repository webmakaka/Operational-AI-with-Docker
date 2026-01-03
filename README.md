# Operational AI with Docker


This is the code repository for **Operational AI with Docker: LLMOps, Agents, and Multi-Model Systems with Docker and Kubernetes**, published by Packt.

**Build, deploy, and scale production-ready AI applications using Docker's integrated AI toolkit**.

## What is this book about?

This comprehensive guide teaches you to operationalize AI applications using Docker's suite of AI tools. From running local LLMs to deploying autonomous agent systems in production, you'll master the complete workflow of building, securing, and scaling AI workloads with Docker Desktop, Model Runner, and MCP Gateway.

This book covers the following exciting features:

* Run and optimize local LLMs with Docker Model Runner
* Integrate AI applications with external systems using MCP (Model Context Protocol)
* Deploy MCP servers securely with Docker MCP Gateway
* Build autonomous AI agents with multi-agent architectures
* Implement production security with Docker Hardened Images
* Monitor AI workloads with Prometheus and Grafana
* Integrate AI with GitHub, Slack, Kubernetes, and databases
* Scale AI applications from development to production
* Implement enterprise security patterns for AI deployments
* Automate AI workflows with Docker Compose and orchestration


## Instructions and Navigations

All of the code is organized into folders by chapter. For example, `chapt-06/` contains all examples for Chapter 6.

The code will look like the following:

```yaml
services:
  gateway:
    image: docker/mcp-gateway
    command:
      - --transport=sse
      - --port=8080
```

**Following is what you need for this book:**

This book is for DevOps engineers, platform engineers, AI/ML engineers, solutions architects, and developers who want to operationalize AI applications. Whether you're deploying your first LLM or building complex multi-agent systems, this book provides practical guidance for production AI with Docker.

A basic understanding of Docker containers and AI concepts is helpful but not required. The book assumes familiarity with command-line tools and includes hands-on examples that work on macOS, Windows, and Linux.











