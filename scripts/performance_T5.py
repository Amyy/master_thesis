# performance calculation of Binary Merkle Tree vs. T5 Tree with different openings
from typing import List


# tree generation formula: standard Merkle Tree
def formula_merkle_tree_gen(leaves: int):
    return leaves - 1


# tree generation formula: T5 Merkle Tree
def t5_tree_gen_formula(leaves: int):
    return 3 / 4 * (leaves - 1)  # ! is float


# Merkle tree: convert list of tree-heights in list of tree-children
def power_of_two(exponents: List[int]):
    powered_list = []
    for element in exponents:
        powered_list.append(pow(2, element))
    return powered_list


def power_of_five(exponents: List[int]):
    powered_list = []
    for element in exponents:
        powered_list.append(pow(5, element))
    return powered_list


if __name__ == '__main__':

    # LMS parameter set for SHA-256, m = 32
    param_set_d = [5, 10, 15, 20, 25]
    leaves_list_binary = power_of_two(param_set_d)
    leaves_list_t5 = power_of_five(param_set_d)
    print('LMS list of possible leaves for binary merkle tree:', leaves_list_binary)
    print('LMS list of possible leaves for t5 tree:', leaves_list_t5)

    hashcalls_treegen_Merkle_LMS_sha256 = []
    hashcalls_treegen_T5 = []
    for leaf_count in leaves_list_binary:
        hashcalls_treegen_Merkle_LMS_sha256.append(formula_merkle_tree_gen(leaf_count))
        hashcalls_treegen_T5.append(t5_tree_gen_formula(leaf_count))

    print('Hash calls keygen. binary Merkle Tree LMS param:', hashcalls_treegen_Merkle_LMS_sha256)
    print('Hash calls keygen. T5 LMS param:', hashcalls_treegen_T5)
