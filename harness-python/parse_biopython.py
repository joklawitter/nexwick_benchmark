#!/usr/bin/env python3
import sys
import os
import time
from Bio import Phylo

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

        trees = list(Phylo.parse(file_path, schema))
        num_trees = len(trees)
        first_leaves = trees[0].count_terminals() if num_trees else 0

        end_time = time.perf_counter()

        print(f"biopython ({schema})")
        print(f"trees={num_trees}, leaves={first_leaves}")
        print(f"time={end_time - start_time:.4f}s")

    except Exception as e:
        print(f"Biopython parsing failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()