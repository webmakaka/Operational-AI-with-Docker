import os
import subprocess
from pathlib import Path

from onnxruntime.quantization import QuantType, quantize_dynamic

MODEL_ID = os.environ.get(
    "MODEL_ID",
    "distilbert/distilbert-base-uncased-distilled-squad",
)
OUT_DIR = Path(os.environ.get("OUT_DIR", "/out")).resolve()
TASK = os.environ.get("TASK", "question-answering")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    onnx_dir = OUT_DIR / "onnx"
    onnx_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "optimum-cli",
        "export",
        "onnx",
        "--model",
        MODEL_ID,
        "--task",
        TASK,
        str(onnx_dir),
    ]
    print(f"[export] Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)

    model_path = onnx_dir / "model.onnx"
    if not model_path.exists():
        raise FileNotFoundError(f"Expected ONNX model at {model_path}")

    quant_path = OUT_DIR / "model.int8.onnx"
    print(f"[quantize] Writing quantized model to: {quant_path}")

    quantize_dynamic(
        model_input=str(model_path),
        model_output=str(quant_path),
        weight_type=QuantType.QInt8,
    )

    print("[done] Export + quantization complete.")
    print(f"[done] Outputs in: {OUT_DIR}")


if __name__ == "__main__":
    main()
