import os
import subprocess
from pathlib import Path

# Configuration
API_KEY = os.environ.get("OPENAI_API_KEY", "")
BASE_DIR = Path(r"d:\Desktop D\Apps\babel-lunartech\babel-lunartech")
INPUT_FILE = BASE_DIR / "test" / "alexandria" / "redmoon" / "input" / "Design and Manufacture of a mini-turbojet.pdf"
OUTPUT_DIR = BASE_DIR / "test" / "alexandria" / "redmoon" / "output"
BABELDOC_DIR = BASE_DIR / "babel-backend" / "BabelDOC-main"

# 22 Popular Languages (ISO 639-1)
# Starting with user-requested ones
LANGUAGES = [
    ("hy", "Armenian"),
    ("nl", "Dutch"),
    ("de", "German"),
    ("ar", "Arabic"),
    ("zh", "Chinese (Mandarin)"),
    ("es", "Spanish"),
    ("fr", "French"),
    ("hi", "Hindi"),
    ("bn", "Bengali"),
    ("pt", "Portuguese"),
    ("ru", "Russian"),
    ("ja", "Japanese"),
    ("pa", "Punjabi"),
    ("mr", "Marathi"),
    ("te", "Telugu"),
    ("tr", "Turkish"),
    ("ko", "Korean"),
    ("vi", "Vietnamese"),
    ("it", "Italian"),
    ("yo", "Yoruba"),
    ("ha", "Hausa"),
    ("id", "Indonesian") # Added Indonesian to reach 22
]

def run_translation(lang_code, lang_name):
    print(f"\n--- Starting translation for {lang_name} ({lang_code}) ---")
    
    cmd = [
        "uv", "run", "babeldoc",
        "--files", str(INPUT_FILE.absolute()),
        "--lang-out", lang_code,
        "--openai",
        "--openai-model", "gpt-4o",
        "--openai-api-key", API_KEY,
        "--pool-max-workers", "4",
        "--output", str(OUTPUT_DIR.absolute())
    ]
    
    try:
        # Using subprocess.run to wait for each translation to finish
        result = subprocess.run(
            cmd,
            cwd=str(BABELDOC_DIR),
            capture_output=True,
            text=True,
            check=True
        )
        print(f"Successfully translated to {lang_name}")
        # print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error translating to {lang_name}: {e}")
        print(f"Stderr: {e.stderr}")

def main():
    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir(parents=True)
    
    for lang_code, lang_name in LANGUAGES:
        run_translation(lang_code, lang_name)

if __name__ == "__main__":
    main()
