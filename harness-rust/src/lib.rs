//! Shared scaffolding for external Rust-based parser benchmark harnesses.
//!
//! Every harness binary needs to parse CLI args, time *only* the parse,
//! and print checksums, while differing only in which library it calls.
//! So the shared part lives here.
//!
//! A binary supplies a single closure `(&Args) -> Counts` and calls [`run`]:
//! ```ignore
//! fn main() -> std::process::ExitCode { harness_rust::run("name", false, parse) }
//! fn parse(args: &harness_rust::Args) -> Result<harness_rust::Counts, _> { ... }
//! ```
//!
//! Output is three lines on stdout:
//! ```text
//! <name><flags>
//! #trees=<n>, #leaves=<n>
//! time=<seconds>s
//! ```

use std::error::Error;
use std::process::ExitCode;
use std::time::Instant;

/// Tree-passing mode requested on the command line.
pub enum Mode {
    /// Parse every tree up front.
    Eager,
    /// Parse one tree at a time, discarding each after counting.
    Lazy,
}

impl std::fmt::Display for Mode {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Mode::Eager => write!(f, "eager"),
            Mode::Lazy => write!(f, "lazy"),
        }
    }
}

/// Tree file format requested on the command line.
pub enum Format {
    /// A NEXUS file with a TREES block.
    Nexus,
    /// A file of bare semicolon-separated Newick strings.
    Newick,
}

impl std::fmt::Display for Format {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Format::Nexus => write!(f, "nexus"),
            Format::Newick => write!(f, "newick"),
        }
    }
}

/// Parsed command-line arguments handed to a harness closure.
pub struct Args {
    /// Path to the trees file to parse.
    pub path: String,
    /// Requested tree-passing mode (parsers that support only one may ignore it).
    pub mode: Mode,
    /// Requested input format (parsers that support only one may error).
    pub format: Format,
}

/// The two checksums every harness reports.
pub struct Counts {
    /// Number of trees parsed.
    pub num_trees: usize,
    /// Leaf count of the first parsed tree (0 if there were none).
    pub first_leaves: usize,
}

/// Entry point for a harness: parses args, times `parse`, prints the report.
///
/// Returns a process exit code so `main` can be `fn main() -> ExitCode`.
pub fn run<F>(name: &str, show_mode: bool, parse: F) -> ExitCode
where
    F: FnOnce(&Args) -> Result<Counts, Box<dyn Error>>,
{
    match run_inner(name, show_mode, parse) {
        Ok(()) => ExitCode::SUCCESS,
        Err(e) => {
            eprintln!("harness: {e}");
            ExitCode::FAILURE
        }
    }
}

fn run_inner<F>(name: &str, show_mode: bool, parse: F) -> Result<(), Box<dyn Error>>
where
    F: FnOnce(&Args) -> Result<Counts, Box<dyn Error>>,
{
    let args = parse_args()?;

    let start = Instant::now();
    let counts = parse(&args)?;
    let elapsed = start.elapsed();

    if show_mode {
        println!("{name} ({}, {})", args.mode, args.format);
    } else {
        println!("{name} ({})", args.format);
    }
    println!("#trees={}, #leaves={}", counts.num_trees, counts.first_leaves);
    println!("time={:.4}s", elapsed.as_secs_f64());
    Ok(())
}

/// Hand-rolled argument parsing: one required positional path plus optional
/// `--eager` / `--lazy` (defaults to eager) and `--nexus` / `--newick`
/// (defaults to nexus) flags. No dependency, so it never adds compile time or
/// code to the binaries being measured.
pub fn parse_args() -> Result<Args, Box<dyn Error>> {
    let mut path: Option<String> = None;
    let mut mode = Mode::Eager;
    let mut format = Format::Nexus;

    for arg in std::env::args().skip(1) {
        match arg.as_str() {
            "--eager" => mode = Mode::Eager,
            "--lazy" => mode = Mode::Lazy,
            "--nexus" => format = Format::Nexus,
            "--newick" => format = Format::Newick,
            _ if arg.starts_with('-') => return Err(format!("unknown flag: {arg}").into()),
            _ if path.is_none() => path = Some(arg),
            _ => return Err(format!("unexpected extra argument: {arg}").into()),
        }
    }

    let path =
        path.ok_or("usage: <harness> <path> [--eager | --lazy] [--nexus | --newick]")?;
    Ok(Args { path, mode, format })
}
