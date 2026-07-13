//! Benchmark harness for the `nexwick` parser
//! for NEXUS files in eager or lazy mode
//! and Newick files in eager mode.

use std::error::Error;
use std::hint::black_box;
use std::process::ExitCode;

use harness_rust::{Args, Counts, Format, Mode};
use nexwick::newick::parse_file;
use nexwick::nexus::NexusParserBuilder;

fn main() -> ExitCode {
    harness_rust::run("nexwick", true, parse)
}

fn parse(args: &Args) -> Result<Counts, Box<dyn Error>> {
    if let Format::Newick = args.format {
        let (trees, _map) = parse_file(&args.path)?;
        let first_leaves = trees.first().map_or(0, |t| black_box(t).num_leaves());
        return Ok(Counts { num_trees: trees.len(), first_leaves });
    }

    let (num_trees, first_leaves) = match args.mode {
        Mode::Eager => {
            let parser = NexusParserBuilder::for_file(&args.path)?.eager().build()?;
            let num_trees = parser.num_trees();
            let (trees, _map) = parser.into_results()?;
            // `num_leaves()` on the tree (not the parser) forces the tree data
            // to be touched, anchoring it against dead-code elimination.
            let first_leaves = trees.first().map_or(0, |t| black_box(t).num_leaves());
            (num_trees, first_leaves)
        }
        Mode::Lazy => {
            let mut parser = NexusParserBuilder::for_file(&args.path)?.lazy().build()?;
            let mut num_trees = 0usize;
            let mut first_leaves = 0usize;
            while let Some(tree) = parser.next_tree()? {
                if num_trees == 0 {
                    first_leaves = tree.num_leaves();
                }
                black_box(&tree);
                num_trees += 1;
            }
            (num_trees, first_leaves)
        }
    };

    Ok(Counts { num_trees, first_leaves })
}