
## Component 1: Reasoning Engine

```shell
$ docker compose up --build
```

## Results:

```
[+] up 3/3
 ✔ Image 01reasoning-node-genai       Built                                 1.4s
 ✔ llama                              Configured                            2.2s
 ✔ Container 01reasoning-node-genai-1 Recreated                             0.1s
Attaching to node-genai-1
node-genai-1  | Server starting on http://localhost:8080
node-genai-1  | Using LLM endpoint: http://172.17.0.1:12434/v1//chat/completions
node-genai-1  | Using model: ai/llama3.2:1B-Q8_0
```

Open http://localhost:8082 in your browser to use the web interface. The interface provides a simple chat box where you can interact with the reasoning engine directly. Each message you send gets processed by the LLM, demonstrating how agents use reasoning engines to understand and respond to inputs.

<br/>

## Test the API endpoint

```shell
$ curl -X POST http://localhost:8082/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain Docker in simple terms"}' | jq
```

## Response

```json
{
  "response": "Docker is a way to package, ship, and run applications in containers. Here's a simple explanation:\n\n**What is a container?**\n\nImagine you're packing a suitcase with all your clothes, books, and other belongings. You want to make sure everything is safe, organized, and easy to move around. A container is like that suitcase. It's a self-contained environment that holds all the necessary files, libraries, and settings to run an application.\n\n**How does Docker work?**\n\nHere's a simplified overview:\n\n1. **Build**: You create a Docker image by installing the necessary dependencies, libraries, and settings in a container. This is like packing your suitcase.\n2. **Run**: You can then use the image as a template to create multiple containers. Each container is like a separate suitcase that runs a specific version of your application.\n3. **Deploy**: When you want to deploy your application to a production environment, you can use Docker to create multiple containers from the same image. This way, you can easily manage and update your application across all containers.\n\n**Benefits of Docker**\n\n1. **Isolation**: Containers help isolate application environments, making it easier to manage and monitor them.\n2. **Portability**: Containers are lightweight and portable, making it easy to move applications between different environments.\n3. **Efficient resource usage**: Containers help optimize resource usage, as they are designed to run as isolated environments.\n\n**Docker concepts**\n\n1. **Images**: Docker images are the base templates that contain all the necessary dependencies and settings for an application.\n2. **Containers**: Containers are the running instances of an application, created from the same image.\n3. **Docker Compose**: Docker Compose is a tool that helps you manage and deploy multiple containers as a single application.\n\nIn simple terms, Docker is a way to package, ship, and run applications in a self-contained environment, making it easier to manage and deploy them across different environments."
}
```
