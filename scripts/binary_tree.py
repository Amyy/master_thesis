# LMS: count hash function calls
# 1 node in tree = 1 hash function call for keygen

from binarytree import Node, tree


if __name__ == '__main__':
    root1 = tree(height=2, is_perfect=True)
    print("Binary tree of given height :")
    print(root1)
    print(root1.leaf_count)  # == 2^height

