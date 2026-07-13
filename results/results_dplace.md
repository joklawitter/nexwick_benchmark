| Command | Mean [ms] | Min [ms] | Max [ms] | Relative |
|:---|---:|---:|---:|---:|
| `harness-rust\target\release\nexwick.exe data/dplace_bourckaert_posterior.trees --lazy --nexus` | 143.1 ± 8.6 | 130.5 | 150.5 | 1.00 |
| `harness-rust\target\release\nexwick.exe data/dplace_bourckaert_posterior.trees --eager --nexus` | 151.5 ± 8.6 | 143.6 | 173.1 | 1.06 ± 0.09 |
| `harness-rust\target\release\cyanea_phylo.exe data/dplace_bourckaert_posterior.trees --nexus` | 259.8 ± 7.7 | 246.2 | 274.5 | 1.82 ± 0.12 |
| `harness-cpp\ncl_harness.exe data/dplace_bourckaert_posterior.trees --nexus` | 474.7 ± 5.4 | 466.5 | 483.3 | 3.32 ± 0.20 |
| `Rscript harness-R\parse_ape.R data/dplace_bourckaert_posterior.trees --nexus` | 1364.0 ± 23.1 | 1322.1 | 1402.8 | 9.53 ± 0.59 |
| `java -cp harness-java;D:/Projects/Phylo/BEAST/lib/packages/*;D:/Projects/Phylo/BEAST/lib/* Beast2Harness data/dplace_bourckaert_posterior.trees --nexus` | 1715.0 ± 20.0 | 1683.9 | 1744.7 | 11.99 ± 0.73 |
| `python harness-python\parse_dendropy_lazy.py data/dplace_bourckaert_posterior.trees --nexus` | 6293.9 ± 63.9 | 6216.3 | 6438.8 | 43.99 ± 2.67 |
| `python harness-python\parse_dendropy.py data/dplace_bourckaert_posterior.trees --nexus` | 7539.5 ± 223.5 | 7194.2 | 7913.3 | 52.70 ± 3.52 |
| `python harness-python\parse_biopython.py data/dplace_bourckaert_posterior.trees --nexus` | 11868.0 ± 332.3 | 11502.1 | 12348.7 | 82.96 ± 5.48 |
