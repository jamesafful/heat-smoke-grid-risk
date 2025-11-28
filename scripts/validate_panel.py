#!/usr/bin/env python
import argparse, json, pandas as pd, pathlib, sys
from jsonschema import validate, Draft202012Validator

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", required=True)
    ap.add_argument("--schema", default="metadata/schema.panel.json")
    args = ap.parse_args()

    sch = json.load(open(args.schema, "r"))
    v = Draft202012Validator(sch)

    df = pd.read_parquet(args.panel)
    errors = []
    for i, row in df.iterrows():
        obj = {k: row[k] for k in sch["properties"].keys() if k in df.columns}
        # coerce date to iso date
        if "date" in obj and not isinstance(obj["date"], str):
            obj["date"] = pd.to_datetime(obj["date"]).date().isoformat()
        try:
            validate(obj, sch)
        except Exception as e:
            errors.append((i, str(e)))
            if len(errors) > 20:  # stop early
                break

    if errors:
        print("Schema validation FAILED. First errors:")
        for i, msg in errors[:10]:
            print(f"row {i}: {msg}")
        sys.exit(1)
    print("Schema validation PASSED.")

if __name__ == "__main__":
    main()
