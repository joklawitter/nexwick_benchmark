| Command | Mean [s] | Min [s] | Max [s] | Relative |
|:---|---:|---:|---:|---:|
| `harness-rust\target\release\nexwick.exe data/cephalopod.gradual.trees --eager --nexus` | 0.607 ± 0.007 | 0.597 | 0.616 | 1.00 |
| `harness-rust\target\release\nexwick.exe data/cephalopod.gradual.trees --lazy --nexus` | 1.035 ± 0.003 | 1.031 | 1.040 | 1.71 ± 0.02 |
| `harness-rust\target\release\cyanea_phylo.exe data/cephalopod.gradual.trees --nexus` | 1.702 ± 0.158 | 1.522 | 1.960 | 2.80 ± 0.26 |
| `harness-cpp\ncl_harness.exe data/cephalopod.gradual.trees --nexus` | 2.103 ± 0.028 | 2.077 | 2.157 | 3.47 ± 0.06 |
| `Rscript harness-R\parse_ape.R data/cephalopod.gradual.trees --nexus` | 5.190 ± 0.011 | 5.177 | 5.210 | 8.55 ± 0.10 |
| `java -cp harness-java;D:/Projects/Phylo/BEAST/lib/packages/*;D:/Projects/Phylo/BEAST/lib/* Beast2Harness data/cephalopod.gradual.trees --nexus` | 8.981 ± 0.118 | 8.815 | 9.232 | 14.80 ± 0.26 |
| `python harness-python\parse_commonnexus.py data/cephalopod.gradual.trees --nexus` | 16.924 ± 0.185 | 16.692 | 17.233 | 28.32 ± 0.40 |
| `python harness-python\parse_dendropy_lazy.py data/cephalopod.gradual.trees --nexus` | 45.946 ± 0.510 | 44.852 | 46.462 | 75.73 ± 1.22 |
| `python harness-python\parse_biopython.py data/cephalopod.gradual.trees --nexus` | 54.267 ± 1.918 | 53.432 | 59.685 | 89.44 ± 3.33 |
| `python harness-python\parse_dendropy.py data/cephalopod.gradual.trees --nexus` | 59.739 ± 1.069 | 58.910 | 62.295 | 98.46 ± 2.10 |

