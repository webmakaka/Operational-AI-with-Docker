# Docker Offload Chapter 4 files

These files support the worked example for Docker Offload model export and quantization.

## Typical flow

```bash
./scripts/01-start-offload.sh
./scripts/02-status-offload.sh
./scripts/03-build-image.sh
./scripts/04-run-export.sh
./scripts/05-diagnose-offload.sh   # optional
./scripts/06-stop-offload.sh
```

## Optional GPU Offload

```bash
./scripts/01-start-offload.sh --gpu
```

## Environment variables

You can override these defaults when running the export script:

```bash
IMAGE_NAME=onnx-export:offload \
MODEL_ID=distilbert/distilbert-base-uncased-distilled-squad \
TASK=question-answering \
./scripts/04-run-export.sh
```
