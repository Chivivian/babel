# BabelDOC Internals

This document provides a technical deep-dive into the BabelDOC translation engine. It explains each stage of the translation pipeline, from PDF parsing to final document reconstruction.

---

## Pipeline Overview

When a document is submitted for translation, it passes through the following stages:

```
┌─────────────────┐
│  1. PDF Parsing │ → Extract text, images, layout metadata
└────────┬────────┘
         ▼
┌─────────────────┐
│ 2. Layout Analysis │ → Identify paragraphs, tables, headers
└────────┬────────┘
         ▼
┌─────────────────┐
│ 3. Term Extraction │ → Build glossary of technical terms
└────────┬────────┘
         ▼
┌─────────────────┐
│ 4. LLM Translation │ → Contextual translation via GPT-4o
└────────┬────────┘
         ▼
┌─────────────────┐
│ 5. Reconstruction │ → Rebuild PDF with translated content
└─────────────────┘
```

---

## Stage 1: PDF Parsing

**Module:** `pdfminer.six` + Custom extractors

**Purpose:** Extract all text, images, and structural metadata from the source PDF.

### What Gets Extracted

| Element | Method |
| :--- | :--- |
| Text blocks | `pdfminer` text extraction |
| Images | Embedded image extraction (JPEG, PNG) |
| Fonts | Font name and size per text block |
| Layout coordinates | Bounding box (x, y, width, height) for each element |

### Output

A JSON intermediate representation (IR) is created:

```json
{
  "pages": [
    {
      "page_number": 1,
      "elements": [
        {"type": "text", "content": "Hello World", "bbox": [50, 700, 200, 715], "font": "Arial", "size": 12},
        {"type": "image", "path": "images/page1_img1.png", "bbox": [300, 100, 500, 300]}
      ]
    }
  ]
}
```

---

## Stage 2: Layout Analysis

**Module:** `DocLayout-YOLO` (ONNX model)

**Purpose:** Identify structural elements (paragraphs, tables, headers, footers) for contextual grouping.

### Detection Classes

| Class | Description |
| :--- | :--- |
| `paragraph` | Body text content |
| `heading` | Section titles (H1, H2, etc.) |
| `table` | Tabular data structures |
| `list` | Bulleted or numbered lists |
| `footer` | Page footers and footnotes |
| `figure_caption` | Captions for images and diagrams |

### Why This Matters

Grouping text into logical blocks prevents awkward mid-sentence breaks during translation. A paragraph is always translated as a single unit to preserve context.

---

## Stage 3: Term Extraction

**Module:** `translation_config.py` + Glossary Engine

**Purpose:** Identify and extract technical terms to ensure consistent translation throughout the document.

### Extraction Logic

1. Scan all extracted text for capitalized phrases and repeated technical terms.
2. Cross-reference with uploaded user glossaries (if any).
3. Build a "term map" that the LLM will use during translation.

### Example Term Map

```json
{
  "API Key": "Clé API",
  "Machine Learning": "Apprentissage automatique",
  "PDF": "PDF"
}
```

> **Note:** Some terms (like "PDF" or "API") are intentionally left untranslated.

---

## Stage 4: LLM Translation

**Model:** OpenAI GPT-4o (default) or Claude 3.5 Sonnet (fallback)

**Purpose:** Translate each text block while preserving meaning, tone, and context.

### Prompt Engineering

Each translation request includes:

1. **The text block** to translate.
2. **Surrounding context** (previous and next paragraphs).
3. **The term glossary** for consistency.
4. **Formatting instructions** (preserve markdown, avoid adding punctuation).

### Parallelization

To maximize speed, BabelDOC translates up to **20 paragraphs in parallel** using a thread pool. This is configurable via the `--pool-max-workers` flag.

### Fallback Logic

If OpenAI returns a rate-limit error, the system automatically retries with exponential backoff. If OpenAI fails entirely, translation falls back to Claude 3.5 Sonnet.

---

## Stage 5: Reconstruction

**Tools:** Pandoc 3.2 + XeLaTeX (TeX Live 2025)

**Purpose:** Rebuild the PDF with translated content while perfectly preserving the original layout.

### Reconstruction Steps

1. **Inject translated text** into the IR JSON at the exact bounding box locations.
2. **Subset fonts** – Only embed the glyphs actually used (reduces file size by ~60%).
3. **Re-render images** – Place original images at their exact coordinates.
4. **Generate PDF** – XeLaTeX produces the final output with fonts for 50+ languages.

### Output Files

BabelDOC generates two output files:

| File | Description |
| :--- | :--- |
| `filename.lang.mono.pdf` | Single-language translated version |
| `filename.lang.dual.pdf` | Side-by-side original and translation |

> **Default:** The API returns the `.mono.pdf` file. Dual-mode can be requested via the `--dual` flag.

---

## Configuration Options

BabelDOC's behavior can be customized via command-line flags:

| Flag | Description | Default |
| :--- | :--- | :--- |
| `--lang-out` | Target language code | Required |
| `--openai-model` | LLM model to use | `gpt-4o` |
| `--pool-max-workers` | Parallel translation threads | `4` |
| `--translate-table-text` | Translate text inside tables | `false` |
| `--skip-scanned-detection` | Skip OCR on scanned documents | `false` |

---

## Performance Benchmarks

| Document Size | Average Time | Notes |
| :--- | :--- | :--- |
| 10 pages | 30-45 seconds | Cached font subsetting |
| 100 pages | 2-4 minutes | Parallel translation |
| 500 pages | 5-8 minutes | GPU burst may be triggered |

---

## Further Reading

- [Worker Orchestration](./worker-orchestration.md) – How translation jobs are distributed.
- [API Reference](./api-reference.md) – Available endpoints.
