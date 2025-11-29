import re
import json
import os
from datetime import datetime

RAW_DIR = "data/raw"
PARSED_DIR = "data/parsed"

os.makedirs(PARSED_DIR, exist_ok=True)

ERROR_PATTERN = re.compile(r"(error|failed|exception|fatal|traceback)", re.IGNORECASE)

def clean_log(text):
    # Remove GitHub Actions timestamps (2025-11-19T15:51:01.0560000Z)
    text = re.sub(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z", "", text)
    # Remove any remaining timestamps like [10:23:45]
    text = re.sub(r"\[\d{2}:\d{2}:\d{2}\]", "", text)
    return text.strip()

def parse_log(log_path):
    with open(log_path, "r", errors="ignore") as f:
        raw = f.read()
    
    cleaned = clean_log(raw)
    error_lines = [l for l in cleaned.splitlines() if ERROR_PATTERN.search(l)]
    return cleaned, error_lines

def main():
    parsed_count = 0
    
    # Walk through all subdirectories in RAW_DIR
    for root, dirs, files in os.walk(RAW_DIR):
        for fname in files:
            # Process both .log and .txt files
            if fname.endswith(".log") or fname.endswith(".txt"):
                full_path = os.path.join(root, fname)
                
                try:
                    cleaned, errors = parse_log(full_path)
                    
                    # Create output filename that includes subdirectory info
                    rel_path = os.path.relpath(full_path, RAW_DIR)
                    safe_name = rel_path.replace(os.path.sep, "_").replace(".", "_")
                    out_name = f"parsed_{safe_name}.json"
                    out_path = os.path.join(PARSED_DIR, out_name)
                    
                    metadata = {
                        "source": "github_actions" if "gha_run" in full_path else "jenkins",
                        "filename": fname,
                        "directory": root,
                        "raw_log_path": full_path,
                        "timestamp": str(datetime.now()),
                        "cleaned_log": cleaned,
                        "error_lines": errors,
                        "error_count": len(errors)
                    }
                    
                    with open(out_path, "w") as f:
                        json.dump(metadata, f, indent=2)
                    
                    print(f"Parsed: {out_path} (found {len(errors)} errors)")
                    parsed_count += 1
                    
                except Exception as e:
                    print(f"Error parsing {full_path}: {e}")
    
    print(f"\nTotal files parsed: {parsed_count}")

if __name__ == "__main__":
    main()
