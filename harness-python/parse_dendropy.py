#!/usr/bin/env python3
import sys
import os
import time
import dendropy

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 parse_dendropy.py <path_to_file.trees>", file=sys.stderr)
        sys.exit(1)

    schema = "newick" if "--newick" in sys.argv[1:] else "nexus"
    file_path = next(a for a in sys.argv[1:] if not a.startswith("--"))
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'", file=sys.stderr)
        sys.exit(1)

    try:
        start_time = time.perf_counter()

        tree_list = dendropy.TreeList.get(
            path=file_path,
            schema=schema,
            extract_comment_metadata=True,
        )
        num_trees = len(tree_list)
        first_leaves = len(tree_list[0].leaf_nodes()) if num_trees else 0

        end_time = time.perf_counter()

        print(f"dendropy ({schema})")
        print(f"trees={num_trees}, leaves={first_leaves}")
        print(f"time={end_time - start_time:.4f}s")

    except Exception as e:
        print(f"Parsing failed: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()