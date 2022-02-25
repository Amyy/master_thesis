# performance calculation of Binary Merkle Tree vs. T5 Tree with different openings
from typing import List


# tree generation standard Merkle Tree
def merkle_tree_gen(leaves: int):
    return leaves - 1


# tree generation T5 Merkle Tree
def t5_tree_gen(leaves: int):
    return 3 / 4 * (leaves - 1)  # ! is float


# Merkle tree: convert list of tree-heights in list of tree-children
def convert_height_to_leaves_merkle(height_list: List[int]):
    leaves_list = []
    for element in height_list:
        leaves_list.append(pow(2, element))
    return leaves_list


if __name__ == '__main__':
    leaves_merkle = 7
    leaves_t5 = 6

    #  LMS parameter sets for SHA-256, m = 32
    LMS_sha256_param_tree_depth = [5, 10, 15, 20, 25]
    LMS_sha256_param_leaves = convert_height_to_leaves_merkle(LMS_sha256_param_tree_depth)
    print('LMS list of possible leaves for SHA-256:', LMS_sha256_param_leaves)

    hashcalls_treegen_Merkle_LMS_sha256 = []
    hashcalls_treegen_T5 = []
    for leaf_count in LMS_sha256_param_leaves:
        hashcalls_treegen_Merkle_LMS_sha256.append(merkle_tree_gen(leaf_count))
        hashcalls_treegen_T5.append(t5_tree_gen(leaf_count))

    print('Hash calls keygen. binary Merkle Tree LMS param:', hashcalls_treegen_Merkle_LMS_sha256)
    print('Hash calls keygen. T5  LMS param:', hashcalls_treegen_T5)
