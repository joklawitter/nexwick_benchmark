//! Benchmark harness for the `cyanea-phylo` parser (NEXUS).
//!
//! Whole-file eager parse, so `args.mode` is ignored. Leaf count is reported as
//! the number of taxa (all trees in a NEXUS file share one taxa set).

use std::error::Error;
use std::hint::black_box;
use std::process::ExitCode;

use harness_rust::{Args, Counts};

fn main() -> ExitCode {
    harness_rust::run("cyanea-phylo", false, parse)
}

fn parse(args: &Args) -> Result<Counts, Box<dyn Error>> {
    let contents = std::fs::read_to_string(&args.path)?;

    // The error type isn't guaranteed to impl std::error::Error, so render it.
    let nexus = cyanea_phylo::nexus::parse(&contents).map_err(|e| format!("parse error: {e:?}"))?;

    // `black_box` on the trees anchors them against dead-code elimination;
    // leaves = taxa count (shared across all trees in a NEXUS file).
    let num_trees = black_box(&nexus.trees).len();
    let first_leaves = nexus.taxa.len();

    Ok(Counts { num_trees, first_leaves })
}
