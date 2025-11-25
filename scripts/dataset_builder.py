import os
import json
import pandas as pd

PARSED_DIR = "data/parsed"
OUT_PATH = "data/datasets/build_dataset.csv"

rows = []

for fname in os.listdir(PARSED_DIR):
    if not fname.endswith(".json"):
        continue

    data = json.load(open(os.path.join(PARSED_DIR, fname)))

    row = {
        "filename": fname,
        "error_text": "\n".join(data["error_lines"]),
        "cleaned_text": data["cleaned_log"],
    }

    # status inference (simple heuristic)
    if "error" in row["error_text"].lower():
        row["status"] = 1
    else:
        row["status"] = 0

    rows.append(row)

df = pd.DataFrame(rows)
df.to_csv(OUT_PATH, index=False)

print("Dataset created at:", OUT_PATH)

