---
description: How to translate a PDF document to multiple languages
---

# Translation Workflow

// turbo-all

## Quick Commands

### Single Language
```powershell
cd "d:\Desktop D\Apps\babel-lunartech\babel-lunartech"
python translate.py "path/to/document.pdf" --lang es
```

### Multiple Languages
```powershell
python translate.py "path/to/document.pdf" --lang es fr de ja ko
```

### All 22 Languages
```powershell
python translate.py "path/to/document.pdf" --all-languages
```

### Custom Output Directory
```powershell
python translate.py "path/to/document.pdf" --lang es --output "./my-translations/"
```

### Without Watermark
```powershell
python translate.py "path/to/document.pdf" --lang es --no-watermark
```

### List Available Languages
```powershell
python translate.py --list-languages
```

## Options

| Option | Short | Description |
|--------|-------|-------------|
| `--lang` | `-l` | Target language code(s) |
| `--all-languages` | `-a` | Translate to all 22 languages |
| `--output` | `-o` | Custom output directory |
| `--no-watermark` | | Skip LunarTech watermark |
| `--list-languages` | | Show all language codes |
