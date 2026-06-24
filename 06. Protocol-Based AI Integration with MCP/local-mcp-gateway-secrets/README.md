## Demonstrating Docker Compose with secrets

### Getting Started

### Step 1. Create a file named .env

```
github.personal_access_token=DUMMY=ghp_your_token_here
firecrawl.api_key=fc_your_key_here
```

### Step 2. Bring up the services

```
docker compose up --build
```

The Gateway accesses GitHub and Firecrawl using credentials from the secret file. The actual secret values never appear in container environment variables or logs. They are injected only when needed.
