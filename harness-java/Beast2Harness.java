import java.io.File;
import java.util.List;

import beast.base.parser.NexusParser;
import beast.base.evolution.tree.Tree;

public class Beast2Harness {
    public static void main(String[] args) throws Exception {
        if (args.length < 1) {
            System.err.println("Usage: java Beast2Harness <path_to_file.trees>");
            System.exit(1);
        }
        String path = args[0];

        long start = System.nanoTime();
        NexusParser parser = new NexusParser();
        parser.parseFile(new File(path));
        long end = System.nanoTime();

        List<Tree> trees = parser.trees;
        int numTrees = trees.size();
        int firstLeaves = numTrees > 0 ? trees.get(0).getLeafNodeCount() : 0;
        double secs = (end - start) / 1e9;

        System.out.println("beast2");
        System.out.println("trees=" + numTrees + ", leaves=" + firstLeaves);
        System.out.printf("time=%.4fs%n", secs);
    }
}