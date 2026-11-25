#!/usr/bin/env python3
"""Gate for Candidate B (news-image-20261125).

Runs build.py twice and checks:
  1. build exits 0 (no overflow / truncation / overlap problems),
  2. two runs produce byte-identical entry.png (determinism),
  3. entry.png is 1024x1024 and <= 1,048,576 bytes,
  4. entry-300px.png exists and is 300x300 (LANCZOS downscale).
No network, no clock, no randomness. Exit 1 on any failure.
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    from PIL import Image
    results = {}
    for run in (1, 2):
        r = subprocess.run([sys.executable, "build.py", "entry.png"],
                           cwd=HERE, capture_output=True, text=True)
        results[f"run{run}_exit"] = r.returncode
        results[f"run{run}_stdout"] = r.stdout.strip()
        if r.returncode != 0:
            print(json.dumps(results, indent=1))
            print(f"FAIL: build run {run} exited {r.returncode}")
            print(r.stderr)
            sys.exit(1)
        results[f"run{run}_sha256"] = sha(os.path.join(HERE, "entry.png"))
    ok = True
    if results["run1_sha256"] != results["run2_sha256"]:
        print("FAIL: non-deterministic bytes across runs")
        ok = False
    size = os.path.getsize(os.path.join(HERE, "entry.png"))
    results["bytes"] = size
    if size > 1048576:
        print("FAIL: entry.png over 1 MiB")
        ok = False
    im = Image.open(os.path.join(HERE, "entry.png"))
    results["size_px"] = im.size
    if im.size != (1024, 1024):
        print("FAIL: entry.png is not 1024x1024")
        ok = False
    p300 = os.path.join(HERE, "entry-300px.png")
    if not os.path.exists(p300):
        print("FAIL: entry-300px.png missing")
        ok = False
    else:
        im3 = Image.open(p300)
        results["size_300px"] = im3.size
        results["bytes_300px"] = os.path.getsize(p300)
        if im3.size != (300, 300):
            print("FAIL: entry-300px.png is not 300x300")
            ok = False
    results["deterministic"] = (
        results["run1_sha256"] == results["run2_sha256"])
    print(json.dumps(results, indent=1))
    print("GATE PASS" if ok else "GATE FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
