#!/usr/bin/env python3
import sys
import os
import time
from commonnexus import Nexus

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 parse_biopython.py <path_to_file.trees>", file=sys.stderr)
        sys.exit(1)

    schema = "newick" if "--newick" in sys.argv[1:] else "nexus"
    file_path = next(a for a in sys.argv[1:] if not a.startswith("--"))
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'", file=sys.stderr)
        sys.exit(1)

    try:
        start_time = time.perf_counter()

        nexus = Nexus.from_file(file_path)
        num_trees = len(nexus.TREES.trees)
        num_leaves = nexus.TAXA.commands['DIMENSIONS'][0].ntax

        end_time = time.perf_counter()

        print(f"commonnexus ({schema})")
        print(f"trees={num_trees}, leaves={num_leaves}")
        print(f"time={end_time - start_time:.4f}s")

    except Exception as e:
        print(f"commonnexus parsing failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()