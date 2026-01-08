import os
import subprocess
from pathlib import Path

# Configuration
SOURCE_DIR = Path("test/Redmoon/Documents Original")
LANG_MAP = {
    "es": Path("test/Redmoon/Documents Trance ES"),
    "it": Path("test/Redmoon/Documents Trance IT"),
    "pr": Path("test/Redmoon/Documents Trance PR")
}
MODEL = "gpt-4o-mini"
WORKERS = 20

def run_translation():
    files = list(SOURCE_DIR.glob("*.pdf"))
    print(f"Found {len(files)} files in {SOURCE_DIR}")
    
    # Translate all languages for each file in one go for speed
    langs = list(LANG_MAP.keys())
    
    for doc in files:
        print(f"\n--- Translating {doc.name} to {', '.join(langs)} ---")
        # Use a temporary output directory to avoid name collisions
        temp_out = Path("test/Redmoon/temp_out")
        temp_out.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            "python", "translate.py",
            str(doc),
            "--lang", *langs,
            "--model", MODEL,
            "--workers", str(WORKERS),
            "--output", str(temp_out)
        ]
        
        try:
            result = subprocess.run(cmd, check=False)
            if result.returncode == 0:
                print(f"Successfully translated {doc.name}")
                # Move files to their respective target directories
                for lang, target_dir in LANG_MAP.items():
                    target_dir.mkdir(parents=True, exist_ok=True)
                    for output_file in temp_out.glob(f"*{lang}*"):
                        output_file.rename(target_dir / output_file.name)
            else:
                print(f"Failed to translate {doc.name} (exit code {result.returncode})")
        except Exception as e:
            print(f"Error executing command for {doc.name}: {e}")
        finally:
            # Clean up temp_out files if any left
            for f in temp_out.glob("*"):
                try: f.unlink()
                except: pass
            try: temp_out.rmdir()
            except: pass

if __name__ == "__main__":
    run_translation()
