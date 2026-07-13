| Command | Mean [ms] | Min [ms] | Max [ms] | Relative |
|:---|---:|---:|---:|---:|
| `harness-rust\target\release\nexwick.exe data/RSV2-n129-10k.trees --lazy --nexus` | 492.3 ± 3.4 | 487.9 | 499.2 | 1.00 |
| `harness-rust\target\release\nexwick.exe data/RSV2-n129-10k.trees --eager --nexus` | 539.5 ± 10.6 | 528.6 | 566.6 | 1.10 ± 0.02 |
| `harness-rust\target\release\cyanea_phylo.exe data/RSV2-n129-10k.trees --nexus` | 749.6 ± 10.7 | 740.5 | 778.6 | 1.52 ± 0.02 |
| `harness-rust\target\release\phylo_nexus.exe data/RSV2-n129-10k.trees --nexus` | 834.4 ± 4.6 | 827.9 | 843.7 | 1.69 ± 0.02 |
| `harness-cpp\ncl_harness.exe data/RSV2-n129-10k.trees --nexus` | 1821.8 ± 7.1 | 1813.7 | 1836.9 | 3.70 ± 0.03 |
| `Rscript harness-R\parse_ape.R data/RSV2-n129-10k.trees --nexus` | 4524.4 ± 41.3 | 4481.5 | 4610.6 | 9.19 ± 0.11 |
| `java -cp harness-java;D:/Projects/Phylo/BEAST/lib/packages/*;D:/Projects/Phylo/BEAST/lib/* Beast2Harness data/RSV2-n129-10k.trees --nexus` | 5446.2 ± 250.6 | 4759.9 | 5625.7 | 11.06 ± 0.51 |
| `python harness-python\parse_dendropy_lazy.py data/RSV2-n129-10k.trees --nexus` | 22034.9 ± 280.6 | 21836.8 | 22755.8 | 44.76 ± 0.65 |
| `python harness-python\parse_dendropy.py data/RSV2-n129-10k.trees --nexus` | 30660.5 ± 15563.5 | 25208.9 | 74942.0 | 62.28 ± 31.62 |
| `python harness-python\parse_biopython.py data/RSV2-n129-10k.trees --nexus` | | 42964.7 ± 1200.5 | 41091.9 | 45245.1 | 87.01 ± 3.49 |
