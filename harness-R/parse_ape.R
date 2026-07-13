#!/usr/bin/env Rscript
# Benchmark harness for the R `ape` parser.

suppressPackageStartupMessages(library(ape))

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) {
  message("Usage: Rscript parse_ape.R <path_to_file.trees> [--newick]")
  quit(status = 1)
}
format <- if ("--newick" %in% args) "newick" else "nexus"
file_path <- args[!startsWith(args, "--")][1]
if (!file.exists(file_path)) {
  message(sprintf("Error: File not found at '%s'", file_path))
  quit(status = 1)
}

tryCatch({
  start_time <- Sys.time()

  trees <- if (format == "newick") read.tree(file_path) else read.nexus(file_path)

  # read.nexus returns a `phylo` for a single tree, `multiPhylo` for many.
  if (inherits(trees, "multiPhylo")) {
    num_trees <- length(trees)
    first_tree <- trees[[1]]
  } else {
    num_trees <- 1L
    first_tree <- trees
  }
  first_leaves <- length(first_tree$tip.label)

  end_time <- Sys.time()
  elapsed <- as.numeric(difftime(end_time, start_time, units = "secs"))

  cat(sprintf("ape (%s)\n", format))
  cat(sprintf("trees=%d, leaves=%d\n", num_trees, first_leaves))
  cat(sprintf("time=%.4fs\n", elapsed))
}, error = function(e) {
  message(sprintf("Parsing failed: %s", conditionMessage(e)))
  quit(status = 1)
})