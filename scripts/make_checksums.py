#!/usr/bin/env python
import argparse, hashlib, pathlib

def sha256(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p,"rb") as f:
        for chunk in iter(lambda: f.read(1<<20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="release/v1.2")
    ap.add_argument("--out",  default="release/v1.2/metadata/checksums.sha256")
    args = ap.parse_args()

    root = pathlib.Path(args.root)
    files = list(root.glob("artifacts/*")) + list(root.glob("derived/*"))
    outp  = pathlib.Path(args.out); outp.parent.mkdir(parents=True, exist_ok=True)
    with open(outp, "w") as w:
        for f in sorted(files):
            w.write(f"{sha256(f)}  {f.relative_to(root)}\n")
    print(f"Wrote {outp}")

if __name__ == "__main__":
    main()
