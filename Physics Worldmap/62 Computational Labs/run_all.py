#!/usr/bin/env python3
"""Run the 13 core teaching labs; exploratory labs 14–16 run separately."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import time


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="use fast smoke-test settings")
    parser.add_argument("--out-dir", type=Path, default=Path("results/all_labs"))
    args = parser.parse_args()

    lab_directory = Path(__file__).resolve().parent
    scripts = sorted(p for p in lab_directory.glob("[0-9][0-9]_*.py")
                     if 1 <= int(p.name[:2]) <= 13)
    if [int(p.name[:2]) for p in scripts] != list(range(1, 14)):
        raise RuntimeError("expected exactly one core lab for each number 01–13")

    start = time.perf_counter()
    for script in scripts:
        destination = args.out_dir / script.stem
        command = [sys.executable, str(script), "--out-dir", str(destination)]
        if args.quick:
            command.append("--quick")
        print(f"\n=== {script.name} ===", flush=True)
        subprocess.run(command, check=True)
    elapsed = time.perf_counter() - start
    print(f"\nPASS all {len(scripts)} computational labs in {elapsed:.1f} s.")


if __name__ == "__main__":
    main()
