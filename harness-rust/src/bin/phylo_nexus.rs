//! Benchmark harness for the `phylo-nexus` parser (crate `nexus`, NEXUS).
//!
//! This parser only has an eager, whole-file mode, so `args.mode` is ignored.

use std::error::Error;
use std::hint::black_box;
use std::process::ExitCode;

use harness_rust::{Args, Counts};
use phylo_nexus::{Lexer, NexusBlock, Parser, Tokens};

fn main() -> ExitCode {
    harness_rust::run("phylo-nexus", false, parse)
}

fn parse(args: &Args) -> Result<Counts, Box<dyn Error>> {
    let contents = std::fs::read_to_string(&args.path)?;

    let lexer = Lexer::new(&contents);
    let tokens = Tokens::new(&lexer);
    let mut parser = Parser::new(tokens);
    // ParsingError is Debug but not std::error::Error, so render it ourselves.
    let nexus = parser.parse().map_err(|e| format!("parse error: {e:?}"))?;

    // Pull tree info out of the TREES block. Leaves = arena nodes with no
    // child; `black_box` on the first tree anchors it against DCE.
    let (num_trees, first_leaves) = nexus
        .blocks
        .iter()
        .find_map(|block| match block {
            NexusBlock::TreesBlock(_translations, trees) => {
                let first_leaves = trees.first().map_or(0, |t| {
                    black_box(t)
                        .tree
                        .iter()
                        .filter(|node| node.first_child().is_none())
                        .count()
                });
                Some((trees.len(), first_leaves))
            }
            _ => None,
        })
        .unwrap_or((0, 0));

    Ok(Counts { num_trees, first_leaves })
}
