| Command | Mean [ms] | Min [ms] | Max [ms] | Relative |
|:---|---:|---:|---:|---:|
| `harness-rust\target\release\nexwick.exe data/aars.gradual.trees --eager --nexus` | 137.9 ± 4.2 | 133.8 | 147.3 | 1.00 |
| `harness-rust\target\release\nexwick.exe data/aars.gradual.trees --lazy --nexus` | 139.1 ± 3.7 | 135.9 | 146.3 | 1.01 ± 0.04 |
| `harness-rust\target\release\cyanea_phylo.exe data/aars.gradual.trees --nexus` | 617.0 ± 11.4 | 602.7 | 639.8 | 4.47 ± 0.16 |
| `harness-cpp\ncl_harness.exe data/aars.gradual.trees --nexus` | 747.3 ± 2.4 | 744.8 | 751.9 | 5.42 ± 0.17 |
| `Rscript harness-R\parse_ape.R data/aars.gradual.trees --nexus` | 2018.9 ± 8.6 | 2009.8 | 2032.8 | 14.63 ± 0.19 |
| `java -cp harness-java;D:/Projects/Phylo/BEAST/lib/packages/*;D:/Projects/Phylo/BEAST/lib/* Beast2Harness data/aars.gradual.trees --nexus` | 3132.7 ± 19.8 | 3091.4 | 3158.5 | 22.72 ± 0.71 |
| `python harness-python\parse_commonnexus.py data/aars.gradual.trees --nexus` | 5839.9 ± 95.7 | 5709.9 | 5965.9 | 41.95 ± 1.04 |
| `python harness-python\parse_biopython.py data/aars.gradual.trees --nexus` | 15227.4 ± 48.6 | 15141.5 | 15321.9 | 110.31 ± 1.43 |
| `python harness-python\parse_dendropy_lazy.py data/aars.gradual.trees --nexus` | 16313.0 ± 106.4 | 16158.3 | 16487.1 | 118.31 ± 3.68 |
| `python harness-python\parse_dendropy.py data/aars.gradual.trees --nexus` | 20701.6 ± 127.3 | 20487.6 | 20841.6 | 150.13 ± 4.66 |


