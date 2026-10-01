FROM python:3.13-alpine
RUN pip install mcp[cli]
WORKDIR /app
COPY main.py ./
CMD ["python", "main.py"]
