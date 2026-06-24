FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 agent

WORKDIR /app

COPY agent.py .

# Set ownership
RUN chown -R agent:agent /app

USER agent

CMD ["python", "-u", "agent.py"]
