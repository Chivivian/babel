#!/usr/bin/env python3
"""
Babel Translator - Unified PDF Translation CLI

Translate documents to multiple languages with a single command.

Usage:
    python translate.py input.pdf --lang es
    python translate.py input.pdf --lang es fr de ja
    python translate.py input.pdf --all-languages
    python translate.py input.pdf --lang es --output ./translations/
    python translate.py input.pdf --lang es --no-watermark
"""

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding for emoji/unicode
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    # Auto-add uv to PATH on Windows
    uv_path = Path.home() / ".local" / "bin"
    if uv_path.exists() and str(uv_path) not in os.environ.get("PATH", ""):
        os.environ["PATH"] = str(uv_path) + os.pathsep + os.environ.get("PATH", "")

# === Configuration ===
BASE_DIR = Path(__file__).parent.resolve()
BABELDOC_DIR = BASE_DIR / "babel-backend" / "BabelDOC-main"
DEFAULT_OUTPUT_DIR = BASE_DIR / "babel-backend" / "Outputs"
ASSETS_DIR = BASE_DIR / "assets"
LOG_FILE = BASE_DIR / "translation_log.txt"

# 22 Popular Languages (ISO 639-1 codes)
ALL_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "nl": "Dutch",
    "ru": "Russian",
    "zh": "Chinese (Mandarin)",
    "ja": "Japanese",
    "ko": "Korean",
    "ar": "Arabic",
    "hi": "Hindi",
    "bn": "Bengali",
    "pa": "Punjabi",
    "mr": "Marathi",
    "te": "Telugu",
    "tr": "Turkish",
    "vi": "Vietnamese",
    "id": "Indonesian",
    "hy": "Armenian",
    "yo": "Yoruba",
}


def load_api_key():
    """Load OpenAI API key from environment or .env file."""
    if "OPENAI_API_KEY" in os.environ:
        return os.environ["OPENAI_API_KEY"]
    
    env_path = BASE_DIR / "babel-backend" / ".env"
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("OPENAI_API_KEY="):
                    key = line.strip().split("=", 1)[1].strip("'\"")
                    os.environ["OPENAI_API_KEY"] = key
                    return key
    return None


def apply_watermark(pdf_path: Path) -> Path:
    """Apply LunarTech watermark to the PDF."""
    try:
        import pymupdf
    except ImportError:
        print("  ⚠️  pymupdf not installed, skipping watermark")
        return pdf_path
    
    black_logo = ASSETS_DIR / "Horizontal Black_1@4x.png"
    white_logo = ASSETS_DIR / "Horizontal White_1@4x.png"
    
    if not black_logo.exists() or not white_logo.exists():
        print(f"  ⚠️  Watermark assets not found in {ASSETS_DIR}, skipping")
        return pdf_path
    
    try:
        doc = pymupdf.open(pdf_path)
        
        for page in doc:
            page_rect = page.rect
            margin_x, margin_y = 20, 20
            wm_width, wm_height = 100, 30
            
            # Position: Bottom Right
            rect = pymupdf.Rect(
                page_rect.width - wm_width - margin_x,
                page_rect.height - wm_height - margin_y,
                page_rect.width - margin_x,
                page_rect.height - margin_y
            )
            
            # Sample background color to choose logo variant
            sample_point = pymupdf.Point(rect.x0 + rect.width/2, rect.y0 + rect.height/2)
            pix = page.get_pixmap(clip=pymupdf.Rect(
                sample_point.x - 5, sample_point.y - 5,
                sample_point.x + 5, sample_point.y + 5
            ))
            
            # Calculate luminance
            luminance = 255
            if pix.n >= 3:
                pixels = list(pix.samples)
                r_sum = g_sum = b_sum = count = 0
                step = pix.n
                for i in range(0, len(pixels), step):
                    r_sum += pixels[i]
                    g_sum += pixels[i+1]
                    b_sum += pixels[i+2]
                    count += 1
                if count > 0:
                    luminance = 0.299 * (r_sum/count) + 0.587 * (g_sum/count) + 0.114 * (b_sum/count)
            
            logo_path = str(white_logo if luminance < 128 else black_logo)
            page.insert_image(rect, filename=logo_path)
            page.insert_link({
                "kind": pymupdf.LINK_URI,
                "from": rect,
                "uri": "https://lunartech.ai"
            })
        
        # Save watermarked version
        watermarked_path = pdf_path.with_suffix(".watermarked.pdf")
        doc.save(watermarked_path)
        doc.close()
        print(f"  ✅ Watermark applied: {watermarked_path.name}")
        return watermarked_path
    
    except Exception as e:
        print(f"  ⚠️  Watermark failed: {e}")
        return pdf_path


def translate_file(input_file: Path, lang_code: str, output_dir: Path, api_key: str, watermark: bool = True) -> bool:
    """Translate a single file to the specified language."""
    lang_name = ALL_LANGUAGES.get(lang_code, lang_code)
    print(f"\n📄 Translating to {lang_name} ({lang_code})...")
    
    cmd = [
        "uv", "run", "babeldoc",
        "--files", str(input_file.absolute()),
        "--lang-out", lang_code,
        "--openai",
        "--openai-model", "gpt-4o",
        "--openai-api-key", api_key,
        "--pool-max-workers", "4",
        "--output", str(output_dir.absolute())
    ]
    
    try:
        process = subprocess.Popen(
            cmd,
            cwd=str(BABELDOC_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Stream output
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"  {output.strip()}")
        
        return_code = process.poll()
        
        if return_code == 0:
            print(f"  ✅ Translation complete: {lang_name}")
            
            # Find and optionally watermark the output
            if watermark:
                mono_pattern = f"{input_file.stem}.{lang_code}.mono.pdf"
                mono_file = output_dir / mono_pattern
                if mono_file.exists():
                    apply_watermark(mono_file)
            
            return True
        else:
            stderr = process.stderr.read()
            print(f"  ❌ Translation failed: {lang_name}")
            print(f"  Error: {stderr[:500]}")
            return False
            
    except Exception as e:
        print(f"  ❌ Exception: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Babel Translator - Translate PDFs to multiple languages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python translate.py document.pdf --lang es
  python translate.py document.pdf --lang es fr de ja
  python translate.py document.pdf --all-languages
  python translate.py document.pdf --lang es --output ./translations/
  python translate.py document.pdf --lang es --no-watermark
        """
    )
    
    parser.add_argument("input", type=str, help="Path to the PDF file to translate")
    parser.add_argument("--lang", "-l", nargs="+", help="Target language code(s), e.g., es fr de")
    parser.add_argument("--all-languages", "-a", action="store_true", help="Translate to all 22 popular languages")
    parser.add_argument("--output", "-o", type=str, help="Output directory (default: babel-backend/Outputs)")
    parser.add_argument("--no-watermark", action="store_true", help="Skip adding LunarTech watermark")
    parser.add_argument("--list-languages", action="store_true", help="List all available language codes")
    
    args = parser.parse_args()
    
    # List languages and exit
    if args.list_languages:
        print("\n📋 Available Languages:\n")
        for code, name in sorted(ALL_LANGUAGES.items(), key=lambda x: x[1]):
            print(f"  {code:5} - {name}")
        return
    
    # Validate input file
    input_file = Path(args.input)
    if not input_file.is_absolute():
        input_file = Path.cwd() / input_file
    
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        sys.exit(1)
    
    # Determine languages
    if args.all_languages:
        languages = list(ALL_LANGUAGES.keys())
    elif args.lang:
        languages = args.lang
    else:
        print("❌ Please specify --lang or --all-languages")
        parser.print_help()
        sys.exit(1)
    
    # Validate language codes
    for lang in languages:
        if lang not in ALL_LANGUAGES:
            print(f"⚠️  Unknown language code: {lang} (will still attempt)")
    
    # Output directory
    output_dir = Path(args.output) if args.output else DEFAULT_OUTPUT_DIR
    if not output_dir.is_absolute():
        output_dir = Path.cwd() / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load API key
    api_key = load_api_key()
    if not api_key:
        print("❌ OPENAI_API_KEY not found. Set it in environment or .env file.")
        sys.exit(1)
    
    # Print summary
    print("\n" + "="*60)
    print("🌍 BABEL TRANSLATOR")
    print("="*60)
    print(f"📁 Input:    {input_file}")
    print(f"📂 Output:   {output_dir}")
    print(f"🗣️  Languages: {len(languages)} - {', '.join(languages[:5])}{'...' if len(languages) > 5 else ''}")
    print(f"🏷️  Watermark: {'No' if args.no_watermark else 'Yes'}")
    print("="*60)
    
    # Run translations
    start_time = time.time()
    successful = []
    failed = []
    
    for lang_code in languages:
        if translate_file(input_file, lang_code, output_dir, api_key, watermark=not args.no_watermark):
            successful.append(lang_code)
        else:
            failed.append(lang_code)
    
    # Summary
    elapsed = time.time() - start_time
    print("\n" + "="*60)
    print("📊 TRANSLATION SUMMARY")
    print("="*60)
    print(f"⏱️  Time: {elapsed/60:.1f} minutes")
    print(f"✅ Successful: {len(successful)}/{len(languages)}")
    if failed:
        print(f"❌ Failed: {', '.join(failed)}")
    print(f"📂 Output: {output_dir}")
    print("="*60)
    
    # Log results
    with open(LOG_FILE, "a") as f:
        f.write(f"\n[{datetime.now().isoformat()}] Translated {input_file.name}\n")
        f.write(f"  Languages: {', '.join(languages)}\n")
        f.write(f"  Successful: {len(successful)}, Failed: {len(failed)}\n")


if __name__ == "__main__":
    main()
