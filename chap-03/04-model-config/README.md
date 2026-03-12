# 04 — Model configuration

Shows `context_size` and `runtime_flags` in the `models:` section.

**context_size**
Sets the maximum token context window. Increasing it raises RAM usage
significantly — only set as large as your use case requires.

```
context_size: 4096   # ~4 GB RAM for a 7B model
context_size: 8192   # ~6 GB RAM — only if you need long conversations
```

**runtime_flags**
Passed directly to the inference engine (llama.cpp flags shown here):

| Flag                    | Effect                                     |
|-------------------------|--------------------------------------------|
| `--threads N`           | CPU threads for inference                  |
| `--temp 0.7`            | Default sampling temperature               |
| `--top-p 0.9`           | Nucleus sampling cutoff                    |
| `--n-gpu-layers N`      | Offload N layers to GPU (partial GPU mode) |
| `--batch-size N`        | Prompt ingestion batch size (default 512)  |
| `--no-prefill-assistant`| Skip assistant role prefill token          |

Equivalent CLI command:
```bash
docker model configure --threads 8 --temp 0.7 --top-p 0.9 ai/smollm2
```
