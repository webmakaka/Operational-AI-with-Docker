
## Component 1: Reasoning Engine

```
docker compose up --build
```

## Results:

```
 => => naming to docker.io/library/reasoning-node-genai:latest                              0.0s
 => => unpacking to docker.io/library/reasoning-node-genai:latest                           0.3s
 => resolving provenance for metadata file                                                  0.0s
[+] up 3/4
 ✔ Image reasoning-node-genai       Built                                                  16.8s
 ⠼ llama                            Configuring                                             0.3s
 ✔ Network reasoning_default        Created                                                 0.0s
 ✔ Container reasoning-node-genai-1 Created                                                 0.2s
Attaching to node-genai-1
node-genai-1  | Server starting on http://localhost:8080
node-genai-1  | Using LLM endpoint: http://model-runner.docker.internal/v1//chat/completions
node-genai-1  | Using model: ai/llama3.2:1B-Q8_0
```

Open http://localhost:8082 in your browser to use the web interface. The interface provides a simple chat box where you can interact with the reasoning engine directly. Each message you send gets processed by the LLM, demonstrating how agents use reasoning engines to understand and respond to inputs.

## Test the API endpoint


```
curl -X POST http://localhost:8082/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain Docker in simple terms"}'
```

## Response

```
{"response":"Docker in Simple Terms\n\nDocker is a popular containerization platform that allows you to package, ship, and run applications in isolated environments. Here's how it works in simple terms:\n\n**What is a Container?**\n\nA container is a self-contained environment that runs a specific version of an application. It's like a virtual machine, but much faster and more secure.\n\n**How Does Docker Work?**\n\nHere's a step-by-step explanation:\n\n1. **Create a Docker Image**: You create a Docker image by writing a set of instructions..
}
```
