from pathlib import Path
import configparser
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "InpaintAI"
METADATA = PLUGIN / "metadata.txt"

errors = []
warnings = []

if not METADATA.exists():
    errors.append("Missing InpaintAI/metadata.txt")
else:
    cfg = configparser.ConfigParser(interpolation=None)
    cfg.read(METADATA, encoding="utf-8")
    general = cfg["general"] if "general" in cfg else {}

    required_local = [
        "name", "qgisMinimumVersion", "description", "about",
        "version", "author"
    ]
    for field in required_local:
        if not str(general.get(field, "")).strip():
            errors.append(f"Missing metadata field: {field}")

    publication_fields = ["email", "homepage", "repository", "tracker"]
    for field in publication_fields:
        if not str(general.get(field, "")).strip():
            warnings.append(f"Publication metadata still missing: {field}")

for forbidden in ["__pycache__", ".git", ".idea", ".vscode"]:
    if any(p.name == forbidden for p in PLUGIN.rglob("*")):
        errors.append(f"Forbidden generated/development directory in plugin: {forbidden}")

for path in sorted(PLUGIN.glob("*.py")):
    try:
        source = path.read_text(encoding="utf-8")
        compile(source, str(path), "exec")
    except Exception as exc:
        errors.append(f"Python compile failed: {path.name}: {exc}")

text = "\n".join(
    p.read_text(encoding="utf-8", errors="ignore")
    for p in PLUGIN.rglob("*")
    if p.is_file() and p.suffix.lower() in {".py", ".txt", ".md"}
)

if re.search(r"\bsk-[A-Za-z0-9_-]{20,}", text):
    errors.append("Possible hardcoded OpenAI secret detected")

if re.search(r"^\s*(from|import)\s+requests\b", text, re.MULTILINE):
    warnings.append("requests import detected; prefer QgsNetworkAccessManager")
if re.search(r"^\s*(from|import)\s+urllib", text, re.MULTILINE):
    warnings.append("urllib import detected; prefer QgsNetworkAccessManager")

print("Validation results")
for item in warnings:
    print(f"WARNING: {item}")
for item in errors:
    print(f"ERROR: {item}")

if errors:
    sys.exit(1)
print("OK: no blocking local validation errors")
