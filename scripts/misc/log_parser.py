import re
import json
import os
from datetime import datetime

RAW_DIR = "data/raw"
PARSED_DIR = "data/parsed"

os.makedirs(PARSED_DIR, exist_ok=True)

ERROR_PATTERN = re.compile(r"(error|failed|exception|fatal|traceback)", re.IGNORECASE)

def clean_log(text):
    # Remove timestamps like [10:23:45] or 2024-01-01 12:00:00
    text = re.sub(r"\[\d{2}:\d{2}:\d{2}\]", "", text)
    text = re.sub(r"\d{4}-\d{2}-\d{2}.*", "", text)
    return text.strip()

def parse_log(log_path):
    with open(log_path, "r", errors="ignore") as f:
        raw = f.read()

    cleaned = clean_log(raw)

    error_lines = [l for l in cleaned.splitlines() if ERROR_PATTERN.search(l)]

    return cleaned, error_lines

def main():
    for fname in os.listdir(RAW_DIR):
        if not fname.endswith(".log"):
            continue

        full_path = os.path.join(RAW_DIR, fname)
        cleaned, errors = parse_log(full_path)

        metadata = {
            "filename": fname,
            "timestamp": str(datetime.now()),
            "raw_log_path": full_path,
            "error_lines": errors,
            "cleaned_log": cleaned
        }

        out_path = os.path.join(PARSED_DIR, fname.replace(".log", ".json"))
        with open(out_path, "w") as f:
            json.dump(metadata, f, indent=2)

        print("Parsed:", out_path)

if __name__ == "__main__":
    main()

