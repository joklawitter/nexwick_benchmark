#!/bin/bash

TYPE="--nexus" 
FILE="data/aars.gradual.trees"  

echo "=== Benchmarking $TYPE Parsers ==="
# Comment out any line to skip that parser. 
cmds=(
 "harness-rust\target\release\nexwick.exe {file} --lazy {type}"
 "harness-rust\target\release\nexwick.exe {file} --eager {type}"
# "harness-rust\target\release\phylo_nexus.exe {file} {type}"
# "harness-rust\target\release\cyanea_phylo.exe {file} {type}"
# "harness-cpp\ncl_harness.exe {file} {type}"
# "java -cp harness-java;D:/Projects/Phylo/BEAST/lib/packages/*;D:/Projects/Phylo/BEAST/lib/* Beast2Harness {file} {type}"
# "python harness-python\parse_dendropy.py {file} {type}"
# "python harness-python\parse_dendropy_lazy.py {file} {type}"
# "python harness-python\parse_biopython.py {file} {type}"
  "python harness-python\parse_commonnexus.py {file} {type}"
# "Rscript harness-R\parse_ape.R {file} {type}"
)

hyperfine --show-output --warmup 3 --runs 10 \
 -L file "$FILE" \
 -L type "$TYPE" \
 --sort mean-time \
 --export-markdown results.md \
 "${cmds[@]}"