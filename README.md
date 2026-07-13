# Benchmark Datasets

Script and harnesses to benchmark speed of different Nexus file parsers. 

> Quick results overview:  
>  `nexwick` < `cyanea` < `phylo-nexus` < `ncl` < `ape` < `BEAST2` < `DendroPy` < `Biopython`

## Parsers

The following packages offer Nexus or Newick file parsing and are thus candidates for testing.
Here those only supporting Newick and some others packages, with reason given below, have been ignored for the benchmarks.

### Rust
- `nexwick` [crate](https://crates.io/crates/nexwick) [github](https://github.com/joklawitter/nexwick/)
  - Supports lazy and eager (flags `--lazy`/`--eager` for harness) modes, Nexus and Newick files of binary trees without internal vertex names
  - Byte-stream based parser without dependencies; fasted in benchmarks (atm)
- `phylo-nexus` [github](https://github.com/tochsner/phylo-nexus)
  - Lexer-based parser using [logos crate](https://crates.io/crates/logos) for Nexus files
  - Not bug free as it fails to parse valid files (throwing wrong errors) and so not fully format compliant with Nexus format as it cannot deal with all comments and annotation
  - Not published on crates.io yet and crate type set to `cdylib`, so requires a fork and manual edits
  - Considered to compare to logos based parser
- `cyanea-phylo` [crate](https://crates.io/crates/cyanea-phylo)
  - Cyanea being a general phylo R&D management platform, with this particular crate offering, among others, tree construction and ML, with parser offering both Nexus and Newick support
- [ignored - Newick only] `newick` [crate](https://crates.io/crates/newick)
- [ignored - Newick only] `phylo` [crate](https://crates.io/crates/phylo)
- [ignored - Newick only] `tree-sitter-newick` [crate](https://crates.io/crates/tree-sitter-newick)
- [ignored - Newick only] `phylotree` [crate](https://crates.io/crates/phylotree) (but has Nexus output)
- [ignored - Newick only] `rust-phylo` [github](https://github.com/acg-team/rust-phylo) (also not published as create yet)

To get them running, just include crate or github in the cargo.toml and build a harness, e.g. using the provided framework file `harness-rust/src/lib.rs`;
then run `cargo build --release`.

### C++
- `ncl` (Nexus Class Library) [github](https://github.com/mtholder/ncl)
  - to get it running (using provided harness):
    - `git clone https://github.com/mtholder/ncl.git ncl-src`
    - e.g. `g++ -O3 -std=c++17 -I ncl-src ncl_harness.cpp ncl-src/ncl/*.cpp -o ncl_harness.exe`
  - Does not accept "-" in taxon names, so requires search-replace with "_" in taxon block and translate block (but don't touch the trees)
- [ignored] `bpp-phyl` [github](https://github.com/BioPP/bpp-phyl) of Bio++ suite
	Offers a Nexus file parser, but ignored because of special build requirements
- [ignored - Newick only] `Genesis` [github](https://github.com/lczech/genesis)

### Python
- `DendroPy` [package](https://pypi.org/project/DendroPy/)
	- Supports lazy and eager modes
- `Biopython` [website](https://biopython.org/) 
	- Failed to parse some other files, but mostly worked
- [ignored - failing] `ete3`
	- Failed to parse valid files

### R
- `ape` [package](https://cran.r-project.org/web/packages/ape/index.html)
  - Other popular R packages for phylogenetics like `phytools` also use it

### Java
- `BEAST2` [website](https://www.beast2.org/)
	- Tested integrated parser, which offers a lot of capabilities beyond those tested here
- [ignored] `JEBL` (Java Evolutionary Biology Library) [github](https://github.com/zachcp/JEBL)
	- Ignored because no development for over 10y 

### Remark

For languages where the compilers might compile away the unused trees, make sure to touch them or use use for example `std::hint::black_box(tree);` (for Rust).

## Test Datasets

So far, benchmarks only on Nexus files obtained as MCMC samples of BEAST2 runs. Files not included in repo, but they are all freely available to download.

### MCMC Samples (Nexus)
- [D-PLACE](https://github.com/D-PLACE/dplace-data/) associated tree sample by [Bouckaert et al. 2018](https://github.com/D-PLACE/dplace-data/blob/master/phylogenies/bouckaert_et_al2018/posterior.trees), file `posterior.tree`
	- ntax = 306, ntrees = 1000, 13 MB
- [Douglas et al.](https://datadryad.org/dataset/doi:10.5061/dryad.sxksn03dj)
	- aars.gradual.trees
		- ntax = 142, ntrees = 1802, 51 MB 
	- cephalopod.gradual.trees
	    - ntax = , ntrees = 9500, 146 MB
- [RSV2 dataset](https://doi.org/10.17608/k6.auckland.27041803) (or obtain your own MCMC sample following from this BEAST2 [tutorial](https://taming-the-beast.org/tutorials/MEP-tutorial/))
	- ntax = 129, ntrees = 10000, 54MB

You can find more datasets for example on [PhyloData](https://phylodata.com/).

### Other Candidates (Newick)
Files containing only lines of Newick trees or one gigantic Newick tree, e.g. Open Tree of Life (OToL), could be considered to compare the Newick parsers.
Not done for now as the large files like OToL contain internal vertex names or are not binary.


## Execution
Run a [hyperfine](https://crates.io/crates/hyperfine) benchmark in you cli or adapt the script provided.

```
hyperfine --show-output --warmup 3 --runs 10 \
  'path\to\parser1 many_trees.tree --nexus' \
  'path\to\other\parser2 man_trees.tree --nexus'
```

## Results
On all four tested datasets, `nexwick` was fasted in both modes, twice in lazy and twice in eager mode first.
Difference were most prominent on `aars.gradual.trees`, with the smallest difference varying among the other files. Note that `phylo-nexus` only ran on `RSV2` as it failed to deal with annotations in the other files.

### Relative performance

1. `nexwick`: Baseline 1.0
2. `cyanea`: 1.52 - 4.47
3. `phylo-nexus`: 1.69 (`RSV2` only)
4. `ncl`: 3.32 - 5.42
5. `ape`: 8.55 - 14.63
6. `BEAST2`: 11.06 - 22.72
7. `DendroPy` (lazy): 43.99 - 118.31
7. `DendroPy` (eager): 52.70 - 150.13
8. `Biopython`: 82.96 - 110.31

![Relative peformance per dataset (bar plot)](plots/relative_grouped.png?raw=true)
![Relative peformance per dataset (heat map)](plots/relative_heatmap.png?raw=true)

For full result tables see `/results`.
