FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY export_and_quantize.py .

ENTRYPOINT ["python", "/app/export_and_quantize.py"]