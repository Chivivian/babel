# Worker Orchestration

This document explains how Babel executes translation workloads. In the current version, **Babel runs entirely on your local machine**, using your own CPU and GPU resources.

---

## Local Execution Model

Babel is designed to run on a single machine without requiring cloud infrastructure. This gives you:

- **Full control** over your data (nothing leaves your machine except API calls to OpenAI)
- **No recurring cloud costs** beyond your OpenAI API usage
- **Simplicity** – no containers, clusters, or orchestration to manage

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           YOUR LOCAL MACHINE                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│   │   CPU       │    │   GPU       │    │   Memory    │    │   Disk      │  │
│   │   Threads   │    │  (Optional) │    │   16+ GB    │    │   SSD       │  │
│   └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘  │
│          │                  │                  │                  │         │
│          └──────────────────┴──────────────────┴──────────────────┘         │
│                                    │                                        │
│                           ┌────────▼────────┐                               │
│                           │   BabelDOC      │                               │
│                           │   Engine        │                               │
│                           └────────┬────────┘                               │
│                                    │                                        │
│                           ┌────────▼────────┐                               │
│                           │   OpenAI API    │ ◄── Only external connection  │
│                           │   (Translation) │                               │
│                           └─────────────────┘                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Hardware Requirements

### Minimum Requirements

| Component | Requirement | Notes |
| :--- | :--- | :--- |
| **CPU** | 4 cores | More cores = faster parallel processing |
| **RAM** | 8 GB | 16 GB recommended for large documents |
| **Disk** | 5 GB free | For temporary files and outputs |
| **GPU** | Not required | Optional, improves layout analysis speed |

### Recommended Configuration

| Component | Recommendation | Benefit |
| :--- | :--- | :--- |
| **CPU** | 8+ cores (Ryzen 7 / Intel i7) | Faster PDF parsing and reconstruction |
| **RAM** | 16-32 GB | Handle 500+ page documents smoothly |
| **GPU** | NVIDIA RTX 3060+ or equivalent | 2-3x faster layout detection (YOLO model) |
| **Disk** | SSD with 20+ GB free | Fast read/write for temporary files |

---

## CPU Utilization

BabelDOC uses multi-threading to maximize CPU usage:

### Parallel Processing

| Task | Default Threads | Configurable |
| :--- | :--- | :--- |
| PDF Parsing | 4 | Yes (`--pool-max-workers`) |
| LLM API Calls | 20 | Yes (`--pool-max-workers`) |
| PDF Reconstruction | 1 | No (XeLaTeX is single-threaded) |

---

## Worker Configuration

Workers control how many parallel API requests BabelDOC makes to OpenAI. More workers = faster translation, but also higher API costs per minute.

### Recommended Worker Settings

| Use Case | Workers | Command |
| :--- | :--- | :--- |
| **Conservative** – Slow, low cost | 4 | `--workers 4` |
| **Balanced** – Good speed/cost ratio | 10 | `--workers 10` |
| **Fast** – Maximum speed | 20 | `--workers 20` |
| **Aggressive** – For large documents | 32 | `--workers 32` |

### Example Commands

**Standard translation (20 workers):**
```bash
python translate.py document.pdf --lang fr
```

**Low-cost translation (4 workers):**
```bash
python translate.py document.pdf --lang fr --workers 4
```

**Maximum speed (32 workers):**
```bash
python translate.py document.pdf --lang fr --workers 32
```

> [!WARNING]
> Using more than 20 workers may trigger OpenAI rate limits on lower-tier API plans. If you encounter `429 Too Many Requests` errors, reduce the worker count.

---

## LLM Models

Babel uses OpenAI models for translation. Two models are currently recommended:

### Recommended Models

| Model | Cost | Quality | Speed | Best For |
| :--- | :--- | :--- | :--- | :--- |
| **gpt-4o-mini** | Low (~$0.15/1M tokens) | Very Good | Fast | Most translations, cost-conscious use |
| **gpt-4o** | Higher (~$2.50/1M tokens) | Excellent | Fast | High-stakes documents, legal/medical |

### Model Selection

**Default model (gpt-4o-mini):**
```bash
python translate.py document.pdf --lang fr
```

**Premium model (gpt-4o):**
```bash
python translate.py document.pdf --lang fr --model gpt-4o
```

### When to Use Each Model

**Use `gpt-4o-mini` (default) when:**
- Translating general business documents
- Cost is a primary concern
- Processing large batches of documents
- Translation quality of 95%+ is acceptable

**Use `gpt-4o` when:**
- Translating legal contracts, medical records, or regulatory documents
- Maximum accuracy is critical
- The document contains highly technical terminology
- You need the best possible quality regardless of cost

### Cost Comparison (Approximate)

| Document Size | gpt-4o-mini | gpt-4o |
| :--- | :--- | :--- |
| 10 pages | ~$0.02 | ~$0.30 |
| 50 pages | ~$0.10 | ~$1.50 |
| 100 pages | ~$0.20 | ~$3.00 |
| 500 pages | ~$1.00 | ~$15.00 |

> [!TIP]
> Start with `gpt-4o-mini` for testing. Switch to `gpt-4o` only for final production translations where quality is paramount.

---

## GPU Utilization (Optional)

If you have an NVIDIA GPU, BabelDOC can use it to accelerate the layout detection step.

### GPU-Accelerated Steps

| Step | Without GPU | With GPU |
| :--- | :--- | :--- |
| Layout Detection (YOLO) | 10-30 seconds | 2-5 seconds |
| PDF Parsing | No change | No change |
| Translation | No change | No change |
| Reconstruction | No change | No change |

### Enabling GPU

GPU acceleration is enabled automatically if:

1. You have an NVIDIA GPU with CUDA support.
2. The ONNX Runtime GPU package is installed.

To verify GPU is being used, check the console output for:
```
Loading ONNX model on GPU...
```

If you see `Loading ONNX model on CPU...`, the system is using CPU mode.

---

## Memory Management

### Memory Usage by Document Size

| Document Size | Peak Memory | Recommendation |
| :--- | :--- | :--- |
| 1-50 pages | 2-4 GB | 8 GB RAM sufficient |
| 50-200 pages | 4-8 GB | 16 GB RAM recommended |
| 200-500 pages | 8-16 GB | 32 GB RAM recommended |
| 500+ pages | 16+ GB | Close other applications |

### Reducing Memory Usage

For very large documents on limited hardware:

```bash
python translate.py large_doc.pdf --lang fr --workers 4
```

Lower worker count reduces memory pressure.

---

## Disk I/O

BabelDOC creates temporary files during processing:

| Directory | Contents | Cleanup |
| :--- | :--- | :--- |
| `babel-backend/Inputs/` | Uploaded source PDFs | Manual |
| `babel-backend/Outputs/` | Translated PDFs | Manual |
| System temp folder | Intermediate files | Automatic |

> **Tip:** Use an SSD for the `babel-backend` directory to improve performance.

---

## Performance Benchmarks (Local Machine)

Tested on: AMD Ryzen 9 5900X, 32 GB RAM, NVIDIA RTX 3080

| Document Size | Translation Time | Notes |
| :--- | :--- | :--- |
| 10 pages | 30-60 seconds | API latency dominates |
| 50 pages | 2-3 minutes | Parallel translation |
| 100 pages | 4-6 minutes | Parallel translation |
| 500 pages | 15-25 minutes | May hit API rate limits |

---

## Future: Cloud Deployment

While Babel currently runs locally, the architecture is designed for future cloud deployment:

- **Railway Pro / Fly.io** – For containerized worker fleets
- **RunPod** – For GPU-accelerated burst capacity
- **Inngest** – For job queue orchestration

These options will be documented when cloud deployment is officially supported.

---

## Further Reading

- [Setup Guide](./setup-guide.md) – Install and configure Babel locally.
- [BabelDOC Internals](./babeldoc-internals.md) – How the translation engine works.
- [Translation Walkthrough](./translation-walkthrough.md) – Step-by-step example.
