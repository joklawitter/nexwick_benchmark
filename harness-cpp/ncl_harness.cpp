#include <chrono>
#include <cstdio>
#include <cstring>

#include "ncl/ncl.h"
#include "ncl/nxsblock.h"
#include "ncl/nxspublicblocks.h"
#include "ncl/nxsmultiformat.h"

int main(int argc, char *argv[]) {
    const char *path = nullptr;
    const char *fmt_name = "nexus";
    bool newick = false;
    for (int i = 1; i < argc; ++i) {
        if (std::strcmp(argv[i], "--newick") == 0) {
            newick = true;
            fmt_name = "newick";
        } else if (std::strcmp(argv[i], "--nexus") == 0) {
            newick = false;
            fmt_name = "nexus";
        } else {
            path = argv[i];
        }
    }
    if (!path) {
        std::fprintf(stderr, "Usage: %s <path_to_file.trees> [--newick]\n", argv[0]);
        return 1;
    }

    MultiFormatReader reader(-1, NxsReader::WARNINGS_TO_STDERR);

    auto start = std::chrono::steady_clock::now();
    try {
        reader.ReadFilepath(path, newick ? MultiFormatReader::RELAXED_PHYLIP_TREE_FORMAT
                                          : MultiFormatReader::NEXUS_FORMAT);
    } catch (const NxsException &e) {
        std::fprintf(stderr, "Parsing failed: %s\n", e.msg.c_str());
        return 1;
    }
    auto end = std::chrono::steady_clock::now();

    unsigned num_trees = 0;
    unsigned first_leaves = 0;
    unsigned n_taxa_blocks = reader.GetNumTaxaBlocks();
    for (unsigned i = 0; i < n_taxa_blocks; ++i) {
        NxsTaxaBlock *taxa = reader.GetTaxaBlock(i);
        if (i == 0) {
            first_leaves = taxa->GetNumTaxonLabels();
        }
        unsigned n_trees_blocks = reader.GetNumTreesBlocks(taxa);
        for (unsigned j = 0; j < n_trees_blocks; ++j) {
            num_trees += reader.GetTreesBlock(taxa, j)->GetNumTrees();
        }
    }

    double secs = std::chrono::duration<double>(end - start).count();
    std::printf("ncl (%s)\n", fmt_name);
    std::printf("trees=%u, leaves=%u\n", num_trees, first_leaves);
    std::printf("time=%.4fs\n", secs);
    return 0;
}
