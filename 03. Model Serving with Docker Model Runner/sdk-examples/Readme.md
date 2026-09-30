# SDK examples

Direct API and SDK examples for Docker Model Runner.

## Prerequisites

```bash
# Pull the model
$ docker model pull ai/smollm2:360M-Q4_K_M

# Warm it up (starts the inference engine)
$ docker model run ai/smollm2:360M-Q4_K_M "hello"
```

## Python

```bash
$ pip install openai
$ python python_sdk.py
```

## Node.js

```bash
$ npm install openai
$ node nodejs_sdk.js
```

## curl

```bash
$ chmod +x curl_examples.sh
$ ./curl_examples.sh
```

<br/>


```json
=== 1. Chat completions ===
{
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Docker is a technology that lets you package and run your software into small containers that can run on different kinds of computers, like Windows, Linux, or Mac. Imagine you have a big box of Lego blocks, each with its own special shape and color. You can stack these Lego blocks together to create a big box.\n\nDocker containers are like Lego blocks that have their own little world with their own tools, operating system, and memory, but they are isolated from each other and from the main computer they're running on. This makes it much easier to test and run different versions of your software, or to quickly switch between different operating systems.\n\nThink of Docker like a magic box that helps you package up your code, and when you want to run it, it automatically runs on your computer just like the real thing. This makes it easier to share your code with other people, or for you to start building new projects quickly.\n\nSo, Docker makes it easier to package, run, and share your software, making it a powerful tool for developers and anyone working with code."
            }
        }
    ],

***
```



## Base URL reference

| Context                          | Base URL                                               |
|----------------------------------|--------------------------------------------------------|
| From host machine                | `http://localhost:12434/engines/v1`                    |
| From Docker container (Compose)  | `http://model-runner.docker.internal/engines/v1`       |
| Alternative (engines path)       | `http://localhost:12434/engines/llama.cpp/v1`          |

No `Authorization` header is required — DMR's local API has no authentication.
