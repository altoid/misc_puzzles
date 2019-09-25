// given a binary tree, find the max path sum between two leaves

class Node {
    int value;
    Node left;
    Node right;

    Node(int v) {
        value = v;
        left = null;
        right = null;
    }
}

class BTree {
    Node root;

    BTree(Node r) {
        root = r;
    }

    private int max_path_sum_helper(Node n) {
        if (n == null) {
            return 0;
        }

        // 3 cases - both children null, both not null, or exactly one null.
        if (n.left == null && n.right == null) {
            return n.value;
        }

        int left_sum = max_path_sum_helper(n.left);
        int right_sum = max_path_sum_helper(n.right);

        if (n.left != null && n.right != null) {
            return Math.max(left_sum, right_sum) + n.value;
        }

        if (n.left != null) {
            return left_sum + n.value;
        }

        return right_sum + n.value;
    }

    int max_path_sum() {
        return max_path_sum_helper(root);
    }
}
