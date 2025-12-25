# Requirements for Babel PDF Translator

## System Requirements
- **Python**: 3.10 - 3.13 (required by BabelDOC)
- **OS**: Windows 10/11, macOS, or Linux
- **RAM**: 8GB minimum (16GB recommended for large PDFs)
- **Disk**: ~2GB for dependencies and models

---

## Package Manager
- **[uv](https://github.com/astral-sh/uv)** - Fast Python package manager (required)

```powershell
# Install uv on Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Python Dependencies (BabelDOC Core)

| Package | Version | Purpose |
|---------|---------|---------|
| `openai` | ≥1.59.3 | OpenAI GPT-4o API for translation |
| `pymupdf` | ≥1.25.1 | PDF parsing and rendering |
| `onnxruntime` | ≥1.16.1 | ML model inference |
| `numpy` | ≥2.0.2 | Numerical operations |
| `opencv-python-headless` | ≥4.10.0 | Image processing |
| `scikit-image` | ≥0.25.2 | Image analysis |
| `scikit-learn` | ≥1.7.1 | Machine learning utilities |
| `tiktoken` | ≥0.9.0 | Token counting for GPT |
| `httpx` | ≥0.27.0 | HTTP client with SOCKS support |
| `huggingface-hub` | ≥0.27.0 | Model downloads |
| `rich` | ≥13.9.4 | Terminal output formatting |
| `tqdm` | ≥4.67.1 | Progress bars |
| `pydantic` | ≥2.10.6 | Data validation |
| `tenacity` | ≥9.0.0 | Retry logic |
| `rapidocr-onnxruntime` | ≥1.4.4 | OCR for scanned PDFs |
| `hyperscan` | ≥0.7.13 | Pattern matching |

### Optional GPU Acceleration
```bash
# For NVIDIA CUDA
uv sync --extra cuda

# For Windows DirectML
uv sync --extra directml
```

---

## Server Dependencies (FastAPI Backend)

| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | latest | Web API framework |
| `uvicorn` | latest | ASGI server |
| `python-multipart` | latest | File upload handling |

```bash
pip install fastapi uvicorn python-multipart
```

---

## Environment Variables

```powershell
# Required - OpenAI API Key
$env:OPENAI_API_KEY = "your-openai-api-key-here"

# Persistent (User level)
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-openai-api-key-here", "User")
```

---

## Quick Install (One-Liner)

```powershell
cd babel-backend/BabelDOC-main; uv sync; cd ..; pip install fastapi uvicorn python-multipart
```

---

## Installation Steps

```bash
# 1. Clone/navigate to project
cd babel-lunartech

# 2. Install BabelDOC dependencies
cd babel-backend/BabelDOC-main
uv sync

# 3. Install server dependencies
cd ..
pip install fastapi uvicorn python-multipart

# 4. Start server
python server.py
```

---

## Frontend
- **No build required** - Static HTML/CSS/JS files
- Served via FastAPI's StaticFiles at `/dashboard`

---

## Running Translation (CLI)

```bash
cd babel-backend/BabelDOC-main
uv run babeldoc --files <input.pdf> --lang-out <lang_code> --openai --openai-model gpt-4o --output <output_dir>
```
