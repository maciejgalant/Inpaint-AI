from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_DIR = ROOT / "InpaintAI"
DIST = ROOT / "dist"
OUTPUT = DIST / "InpaintAI.zip"

EXCLUDED_PARTS = {"__pycache__", ".git", ".idea", ".vscode"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}


def should_include(path: Path) -> bool:
    rel = path.relative_to(PLUGIN_DIR)
    if any(part in EXCLUDED_PARTS for part in rel.parts):
        return False
    if path.suffix.lower() in EXCLUDED_SUFFIXES:
        return False
    return path.is_file()


def main():
    DIST.mkdir(parents=True, exist_ok=True)
    if OUTPUT.exists():
        OUTPUT.unlink()

    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(PLUGIN_DIR.rglob("*")):
            if should_include(path):
                archive.write(path, Path("InpaintAI") / path.relative_to(PLUGIN_DIR))

    print(f"Built: {OUTPUT}")


if __name__ == "__main__":
    main()
