# Chapter 1: Docker Desktop - The Runtime Foundation for AI/ML Workflows

This chapter introduces Docker Desktop as the foundation for running AI/ML workflows. It contains two example applications that demonstrate basic Docker usage for different types of workloads.

## Available Folders

### 1. `tiny-service-container`

A lightweight FastAPI web service that provides a health check endpoint. This example demonstrates containerizing a simple REST API service using Docker.

#### Application Details

- **Framework**: FastAPI
- **Language**: Python 3.11
- **Purpose**: Simple web service with a health check endpoint
- **Endpoint**: `/health` - Returns `{"ok": True}` when the service is running
- **Port**: 8000

The application consists of:
- `app.py`: FastAPI application with a single health endpoint
- `Dockerfile`: Container definition using Python 3.11-slim base image

#### Build Command

Navigate to the `tiny-service-container` directory and build the Docker image:

```bash
cd tiny-service-container
docker build -t tiny-service:latest .
```

Or from the `chap-01` directory:

```bash
docker build -t tiny-service:latest -f tiny-service-container/Dockerfile tiny-service-container/
```

#### Run Command

Start the container and expose port 8000:

```bash
docker run -d -p 8000:8000 --name tiny-service tiny-service:latest
```

To run in the foreground (see logs directly):

```bash
docker run -p 8000:8000 --name tiny-service tiny-service:latest
```

#### Test the Service

Once running, test the health endpoint:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"ok":true}
```

#### Stop and Remove Container

```bash
docker stop tiny-service
docker rm tiny-service
```

---

### 2. `tiny-training-run`

A machine learning training script that trains a Logistic Regression model on the Iris dataset using scikit-learn. This example demonstrates containerizing an ML training workload that runs to completion.

#### Application Details

- **Language**: Python 3.11
- **Libraries**: scikit-learn, numpy
- **Purpose**: Train a machine learning model on the Iris dataset
- **Model**: Logistic Regression classifier
- **Dataset**: Iris dataset
- **Output**: Prints the model's accuracy score on the test set

The application consists of:
- `train.py`: Training script that loads the Iris dataset, splits it into train/test sets, trains a Logistic Regression model and prints the accuracy
- `Dockerfile`: Container definition with dependencies from `requirements.txt`
- `requirements.txt`: Python dependencies (scikit-learn, numpy)

#### Build Command

Navigate to the `tiny-training-run` directory and build the Docker image:

```bash
cd tiny-training-run
docker build -t tiny-training:latest .
```

Or from the `chap-01` directory:

```bash
docker build -t tiny-training:latest -f tiny-training-run/Dockerfile tiny-training-run/
```

#### Run Command

Run the training container (it will execute the training script and exit):

```bash
docker run --name tiny-training tiny-training:latest
```

To view the output and ensure it runs in the foreground:

```bash
docker run --rm tiny-training:latest
```

The `--rm` flag automatically removes the container after it exits.

#### Expected Output

You should see output similar to:

```
accuracy=0.974
```

This indicates the model achieved approximately 97.4% accuracy on the test set.

#### View Container Logs (if run in detached mode)

If you ran the container in detached mode (`-d` flag), you can view the logs:

```bash
docker logs tiny-training
```

#### Remove Container

If the container was not automatically removed:

```bash
docker rm tiny-training
```

---

## Quick Reference Commands

### tiny-service-container

```bash
# Build
cd tiny-service-container
docker build -t tiny-service:latest .

# Run
docker run -d -p 8000:8000 --name tiny-service tiny-service:latest

# Test
curl http://localhost:8000/health

# Stop and remove
docker stop tiny-service && docker rm tiny-service
```

### tiny-training-run

```bash
# Build
cd tiny-training-run
docker build -t tiny-training:latest .

# Run
docker run --rm tiny-training:latest

# View logs (if not using --rm)
docker logs tiny-training
```

---

## Notes

- Both examples use Python 3.11-slim as the base image for a lightweight container
- The service container runs continuously and can be accessed via HTTP
- The training container runs once and exits after completing the training task
- These examples also demonstrate the fundamental difference between long-running services and batch processing workloads in Docker
