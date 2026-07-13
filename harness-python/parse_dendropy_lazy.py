#!/usr/bin/env python3
import sys
import os
import time
import dendropy

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 parse_dendropy_lazy.py <path_to_file.trees>", file=sys.stderr)
        sys.exit(1)

    schema = "newick" if "--newick" in sys.argv[1:] else "nexus"
    file_path = next(a for a in sys.argv[1:] if not a.startswith("--"))
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'", file=sys.stderr)
        sys.exit(1)

    try:
        start_time = time.perf_counter()
        num_trees = 0
        first_leaves = 0

        tree_yielder = dendropy.Tree.yield_from_files(
            files=[file_path],
            schema=schema,
        )
        for tree in tree_yielder:
            if num_trees == 0:
                first_leaves = len(tree.leaf_nodes())
            num_trees += 1

        end_time = time.perf_counter()

        print(f"dendropy (lazy, {schema})")
        print(f"trees={num_trees}, leaves={first_leaves}")
        print(f"time={end_time - start_time:.4f}s")

    except Exception as e:
        print(f"Streaming failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()