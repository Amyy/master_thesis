# performance calculation of Binary Merkle Tree, T5 Tree, T5 Tree+
from typing import List
import math


# tree generation hash calls: standard Merkle Tree
def merkle_tree_gen_hash_calls(merkle_leaves_list: List[int]):
    merkle_tree_gen_hash_call_list = []
    for leaves in merkle_leaves_list:
        merkle_tree_gen_hash_call_list.append(leaves - 1)
    return merkle_tree_gen_hash_call_list


# auth.path length + hash calls verify: standard Merkle Tree
# is same calculation for: auth.path length, hash calls verify
def merkle_tree_len_auth_path_and_verify(merkle_leaves_list: List[int]):
    merkle_tree_len_auth_path_and_verify_list = []
    for leaves in merkle_leaves_list:
        merkle_tree_len_auth_path_and_verify_list.append(math.log2(leaves))  # == 1.443 * log(leaves)
    return merkle_tree_len_auth_path_and_verify_list  # ! returns float


# tree generation hash calls: T5 Merkle Tree
def t5_tree_gen_hash_calls(t5_leaves_list: List[int]):
    t5_tree_gen_hash_calls_list = []
    for leaves in t5_leaves_list:
        t5_tree_gen_hash_calls_list.append(3 / 4 * (leaves - 1))
    return t5_tree_gen_hash_calls_list  # ! returns float


# auth.path length: t5 tree with aggressive opening
def t5_tree_aggr_len_auth_path(t5_leaves_list: List[int]):
    t5_tree_aggr_len_auth_path_list = []
    for leaves in t5_leaves_list:
        t5_tree_aggr_len_auth_path_list.append(3 * math.log(leaves, 5))  # == 1.86 * log(leaves)
    return t5_tree_aggr_len_auth_path_list  # ! returns float


# auth.path length: t5 tree with more aggressive opening
def t5_tree_more_aggr_len_auth_path(t5_leaves_list: List[int]):
    t5_tree_more_aggr_len_auth_path_list = []
    for leaves in t5_leaves_list:
        t5_tree_more_aggr_len_auth_path_list.append(2.8 * math.log(leaves, 5))  # == 1.74 * log(leaves)
    return t5_tree_more_aggr_len_auth_path_list


# verify t5 aggressive: hash calls for path calculation
def t5_tree_aggr_verify(t5_leaves_list: List[int]):
    t5_aggr_verify_hash_calls_list = []
    for leaves in t5_leaves_list:
        t5_aggr_verify_hash_calls_list.append(2 * math.log(leaves, 5))  # == 1.24 * log(leaves)
    return t5_aggr_verify_hash_calls_list


# verify t5 more aggressive: hash calls for path calculation
def t5_tree_more_aggr_verify(t5_leaves_list: List[int]):
    t5_more_aggr_verify_hash_calls_list = []
    for leaves in t5_leaves_list:
        t5_more_aggr_verify_hash_calls_list.append(1.8 * math.log(leaves, 5))  # == 1.12 * log(leaves)
    return t5_more_aggr_verify_hash_calls_list


# Merkle tree: convert list of tree-heights in list of leaves
def power_of_two(exponents: List[int]):
    powered_list = []
    for element in exponents:
        powered_list.append(pow(2, element))
    return powered_list


# t5 tree: convert list of tree-heights in list of leaves
def power_of_five(exponents: List[int]):
    powered_list = []
    for element in exponents:
        powered_list.append(pow(5, element))
    return powered_list


if __name__ == '__main__':
    param_set_d = [5, 10, 15, 20, 25]  # height in LMS parameter set for standard Merkle tree
    lower_bound_d = [11, 23, 34, 46, 58]  # height in LMS parameter set for lower bound Merkle trees
    upper_bound_d = [12, 24, 35, 47, 59]  # height in LMS parameter set for upper bound Merkle trees

    # lists of possible leaves for each tree construct,
    # based on LMS param. set
    leaves_list_merkle_standard = power_of_two(param_set_d)
    leaves_list_t5 = power_of_five(param_set_d)
    leaves_list_low_bound = power_of_two(lower_bound_d)
    leaves_list_up_bound = power_of_two(upper_bound_d)

    # print('LMS list of possible leaves for binary merkle tree:', leaves_list_merkle_standard)
    # print('LMS list of possible leaves for t5 tree:', leaves_list_t5)
    # print('upper bound leaves:', leaves_list_up_bound)
    # print('lower bound leaves:', leaves_list_low_bound)

    # ---- hash calls tree generation ----
    # hash calls tree generation: merkle tree
    hash_calls_tree_gen_merkle_tree = merkle_tree_gen_hash_calls(leaves_list_merkle_standard)
    hash_calls_tree_gen_low_bound = merkle_tree_gen_hash_calls(leaves_list_low_bound)
    hash_calls_tree_gen_up_bound = merkle_tree_gen_hash_calls(leaves_list_up_bound)
    # hash calls tree generation: t5 tree
    hash_calls_tree_gen_T5 = t5_tree_gen_hash_calls(leaves_list_t5)

    # get int values for hash calls in t5 -> only when leaves are power of 5!
    hash_calls_tree_gen_T5 = [int(leaves) for leaves in hash_calls_tree_gen_T5]

    print('merkle tree: hash calls tree gen.', hash_calls_tree_gen_merkle_tree)
    print('lower bound merkle tree: hash calls tree gen.', hash_calls_tree_gen_low_bound)
    print('upper bound merkle tree: hash calls tree gen.', hash_calls_tree_gen_up_bound)
    print('t5 tree: hash calls tree gen.', hash_calls_tree_gen_T5)

    # ---- auth.path length ----
    # amount elements in auth.path: merkle tree
    len_auth_path_list_merkle_tree = merkle_tree_len_auth_path_and_verify(leaves_list_merkle_standard)
    len_auth_path_list_up_bound = merkle_tree_len_auth_path_and_verify(leaves_list_up_bound)
    len_auth_path_list_low_bound = merkle_tree_len_auth_path_and_verify(leaves_list_low_bound)
    # amount elements in auth.path: t5 tree / aggressive
    len_auth_path_list_t5_aggr = t5_tree_aggr_len_auth_path(leaves_list_t5)
    # amount elements in auth.path: t5 tree / more aggressive
    len_auth_path_list_t5_more_aggr = t5_tree_more_aggr_len_auth_path(leaves_list_t5)

    print('merkle tree: length auth.path:', len_auth_path_list_merkle_tree)
    print('lower bound: length auth.path:', len_auth_path_list_low_bound)
    print('upper bound: length auth.path:', len_auth_path_list_up_bound)
    print('t5/aggr: length auth.path:', len_auth_path_list_t5_aggr)
    print('t5/more aggr: length auth.path:', len_auth_path_list_t5_more_aggr)

    # ---- hash calls verify ----
    # Merkle tree: hash calls for path generation / verify
    # for Merkle tree: is same calculation as for length of auth.path
    hash_calls_verify_merkle_tree = len_auth_path_list_merkle_tree
    hash_calls_verify_low_bound = len_auth_path_list_low_bound
    hash_calls_verify_up_bound = len_auth_path_list_up_bound
    # t5 / aggressive: hash calls for path generation / verify
    hash_calls_verify_t5_aggr = t5_tree_aggr_verify(leaves_list_t5)
    # t5 / more aggressive: hash calls for path generation / verify
    hash_calls_verify_t5_more_aggr = t5_tree_more_aggr_verify(leaves_list_t5)

    print('Merkle tree: hash calls verify', hash_calls_verify_merkle_tree)
    print('upper bound: hash calls verify', hash_calls_verify_up_bound)
    print('lower bound: hash calls verify', hash_calls_verify_low_bound)
    print('t5/aggr: hash calls verify', hash_calls_verify_t5_aggr)
    print('t5/more aggr: hash calls verify', hash_calls_verify_t5_more_aggr)