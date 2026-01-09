# Translation Folder

This folder is for translating your documents.

## Usage

1. **Place your PDF files** in the `input/` subfolder
2. **Run the translation command** from the project root:
   ```bash
   python translate.py translate/input/your-document.pdf --lang fr --output translate/output
   ```
3. **Find your translated files** in the `output/` subfolder

## Folder Structure

```
translate/
├── input/      ← Drop your source PDFs here
├── output/     ← Translated PDFs appear here
└── README.md   ← This file
```

## Example

```bash
# Translate a document to Spanish
python translate.py translate/input/manual.pdf --lang es --output translate/output

# Translate to multiple languages
python translate.py translate/input/manual.pdf --lang es fr de --output translate/output
```
