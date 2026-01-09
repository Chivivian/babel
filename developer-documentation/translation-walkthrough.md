# Translation Walkthrough

This document provides a step-by-step walkthrough of the complete translation process, using a real example: translating a technical PDF about jet engine design from English to French.

---

## Example File

**Source Document:** `DESIGN AND FABRICATION OF JET ENGINE USING.pdf`  
**Location:** `test/Redmoon/Documents Original/`  
**Target Language:** French (`fr`)

---

## Overview

When you run a translation, the following stages are executed in sequence:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ 1. CLI Invocation                                                            │
│    python translate.py document.pdf --lang fr                                │
└──────────────────────────────────────────────┬───────────────────────────────┘
                                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 2. Environment Setup                                                         │
│    Load API key, resolve paths, validate input                               │
└──────────────────────────────────────────────┬───────────────────────────────┘
                                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 3. BabelDOC Invocation                                                       │
│    uv run babeldoc --files document.pdf --lang-out fr ...                    │
└──────────────────────────────────────────────┬───────────────────────────────┘
                                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 4. PDF Parsing & Layout Analysis                                             │
│    Extract text, images, detect tables/headers                               │
└──────────────────────────────────────────────┬───────────────────────────────┘
                                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 5. LLM Translation                                                           │
│    Send paragraphs to GPT-4o with context and glossary                       │
└──────────────────────────────────────────────┬───────────────────────────────┘
                                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 6. PDF Reconstruction                                                        │
│    Rebuild PDF with translated text, original layout, and fonts              │
└──────────────────────────────────────────────┬───────────────────────────────┘
                                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 7. Watermarking (Optional)                                                   │
│    Apply LunarTech logo to each page                                         │
└──────────────────────────────────────────────┬───────────────────────────────┘
                                               ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│ 8. Output                                                                    │
│    Save to: DESIGN AND FABRICATION OF JET ENGINE USING.fr.mono.pdf          │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Walkthrough

### Step 1: CLI Invocation

The user runs the translation command:

```bash
python translate.py "test/Redmoon/Documents Original/DESIGN AND FABRICATION OF JET ENGINE USING.pdf" --lang fr
```

**What happens:**
- The `translate.py` script is invoked.
- The `--lang fr` flag specifies French as the target language.

---

### Step 2: Environment Setup

**File:** `translate.py`

The script performs the following setup tasks:

1. **Resolve the input path** – Converts the relative path to an absolute path.
2. **Load the API key** – Reads `OPENAI_API_KEY` from `babel-backend/.env`.
3. **Validate the input file** – Ensures the PDF exists and is readable.
4. **Prepare the output directory** – Defaults to `babel-backend/Outputs/`.

**Console Output:**
```
============================================================
🌍 BABEL TRANSLATOR
============================================================
📁 Input:    d:\...\DESIGN AND FABRICATION OF JET ENGINE USING.pdf
📂 Output:   d:\...\babel-backend\Outputs
🗣️  Languages: 1 - fr
🏷️  Watermark: Yes
============================================================

🚀 Starting translation of 1 languages...
```

---

### Step 3: BabelDOC Invocation

**File:** `translate.py` → `translate_file()` function

The script constructs and executes the following command:

```bash
uv run babeldoc \
  --files "/absolute/path/to/document.pdf" \
  --lang-out fr \
  --openai \
  --openai-model gpt-4o-mini \
  --openai-api-key sk-... \
  --pool-max-workers 20 \
  --qps 20 \
  --output "/absolute/path/to/babel-backend/Outputs"
```

**Explanation of flags:**

| Flag | Value | Purpose |
| :--- | :--- | :--- |
| `--files` | Path to PDF | The document to translate |
| `--lang-out` | `fr` | Target language code |
| `--openai` | — | Use OpenAI for translation |
| `--openai-model` | `gpt-4o-mini` | Model to use (can be `gpt-4o` for higher quality) |
| `--pool-max-workers` | `20` | Parallel translation threads |
| `--qps` | `20` | Queries per second limit |
| `--output` | Directory path | Where to save the output |

---

### Step 4: PDF Parsing & Layout Analysis

**Module:** `BabelDOC-main` (internal)

BabelDOC performs the following:

1. **Load the PDF** – Open the file with `pdfminer.six`.
2. **Extract all text blocks** – Each block includes:
   - Text content
   - Font name and size
   - Bounding box coordinates (x, y, width, height)
3. **Extract images** – Embedded images are saved to a temporary directory.
4. **Run layout detection** – `DocLayout-YOLO` model identifies:
   - Paragraphs
   - Headings
   - Tables
   - Figures and captions

**Console Output:**
```
📄 Translating to French (fr)...
  Loading ONNX model...
  Parse PDF and Create Intermediate Representation
  DetectScannedFile
  Parse Page Layout
  Parse Paragraphs
  Parse Formulas and Styles
```

---

### Step 5: LLM Translation

**Module:** `BabelDOC-main` → Translation engine

For each paragraph, BabelDOC:

1. **Constructs a prompt** including:
   - The paragraph text
   - Surrounding context (previous/next paragraphs)
   - Technical glossary (if provided)
2. **Sends the request** to OpenAI GPT-4o-mini.
3. **Receives the translation** and stores it.

**Parallelization:**
- Up to 20 paragraphs are translated simultaneously.
- Progress is reported in real-time.

**Console Output:**
```
  Automatic Term Extraction
  Translate Paragraphs
  ████████████████████░░░░░░░░░░ 65% | Translating...
```

---

### Step 6: PDF Reconstruction

**Tools:** Pandoc + XeLaTeX

Once all paragraphs are translated:

1. **Inject translated text** – Replace original text blocks with translations.
2. **Preserve layout** – All elements remain at their exact original positions.
3. **Subset fonts** – Only include the character glyphs actually used.
4. **Render the PDF** – XeLaTeX produces the final document.

**Console Output:**
```
  Typesetting
  Add Fonts
  Generate drawing instructions
  Subset font
  Save PDF
```

---

### Step 7: Watermarking (Optional)

**File:** `translate.py` → `apply_watermark()` function

By default, the LunarTech logo is added to the bottom-right corner of each page:

1. **Load the logo** – `assets/Horizontal Black_1@4x.png` or white variant.
2. **Detect background color** – Sample the target area to choose the appropriate logo.
3. **Insert the logo** – Using `pymupdf`.
4. **Add a hyperlink** – Clicking the logo opens `https://lunartech.ai`.

**Output file:**
```
DESIGN AND FABRICATION OF JET ENGINE USING.fr.mono.watermarked.pdf
```

---

### Step 8: Output

**Location:** `babel-backend/Outputs/`

The final translated files are saved:

| File | Description |
| :--- | :--- |
| `...fr.mono.pdf` | Single-language translated PDF |
| `...fr.dual.pdf` | Side-by-side original + translation |
| `...fr.mono.watermarked.pdf` | With LunarTech logo |

**Console Output:**
```
  ✅ Translation complete: French
  ✅ Watermark applied: DESIGN AND FABRICATION OF JET ENGINE USING.fr.mono.watermarked.pdf

============================================================
📊 TRANSLATION SUMMARY
============================================================
⏱️  Time: 2.3 minutes
✅ Successful: 1/1
📂 Output: d:\...\babel-backend\Outputs
============================================================
```

---

## Logging

All translation activity is logged to:
```
logs/translation_log.txt
```

Example log entry:
```
[2025-11-19T14:32:00] Translated DESIGN AND FABRICATION OF JET ENGINE USING.pdf
  Languages: fr
  Successful: 1, Failed: 0
```

---

## Summary

| Stage | Duration (typical) | Key Files |
| :--- | :--- | :--- |
| CLI Invocation | <1 sec | `translate.py` |
| Environment Setup | <1 sec | `babel-backend/.env` |
| BabelDOC Invocation | <1 sec | `babel-backend/BabelDOC-main/` |
| PDF Parsing | 5-15 sec | Internal |
| LLM Translation | 1-4 min | OpenAI API |
| PDF Reconstruction | 10-30 sec | Pandoc, XeLaTeX |
| Watermarking | <5 sec | `pymupdf` |
| **Total** | **2-5 min** | — |

---

## Related Documentation

- [API Reference](./api-reference.md) – For web-based translation via the server.
- [BabelDOC Internals](./babeldoc-internals.md) – Deep-dive into the translation engine.
- [Setup Guide](./setup-guide.md) – How to set up the development environment.
