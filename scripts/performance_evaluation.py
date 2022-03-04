# performance calculation of Binary Merkle Tree, T5 Tree, T5 Tree+
from typing import List
import math
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 15})


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
        t5_tree_aggr_len_auth_path_list.append(round(3 * math.log(leaves, 5)))  # == 1.86 * log(leaves)
    return t5_tree_aggr_len_auth_path_list  # ! returns float


# auth.path length: t5 tree with more aggressive opening
def t5_tree_more_aggr_len_auth_path(t5_leaves_list: List[int]):
    t5_tree_more_aggr_len_auth_path_list = []
    for leaves in t5_leaves_list:
        t5_tree_more_aggr_len_auth_path_list.append(round(2.8 * math.log(leaves, 5)))  # == 1.74 * log(leaves)
    return t5_tree_more_aggr_len_auth_path_list


# verify t5 aggressive: hash calls for path calculation
def t5_tree_aggr_verify(t5_leaves_list: List[int]):
    t5_aggr_verify_hash_calls_list = []
    for leaves in t5_leaves_list:
        t5_aggr_verify_hash_calls_list.append(round(2 * math.log(leaves, 5)))  # == 1.24 * log(leaves)
    return t5_aggr_verify_hash_calls_list


# verify t5 more aggressive: hash calls for path calculation
def t5_tree_more_aggr_verify(t5_leaves_list: List[int]):
    t5_more_aggr_verify_hash_calls_list = []
    for leaves in t5_leaves_list:
        t5_more_aggr_verify_hash_calls_list.append(round(1.8 * math.log(leaves, 5)))  # == 1.12 * log(leaves)
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


# NIST parameter: evaluation results plotted
def plot_hash_calls_tree_gen(merkle_leaves: List[int], low_bound_leaves: List[int],
                             up_bound_leaves: List[int],
                             merkle_hash_calls: List[int], low_bound_hash_calls: List[int],
                             up_bound_hash_calls: List[int]):
    # merkle tree plot
    x1 = merkle_leaves
    y1 = merkle_hash_calls
    plt.plot(x1, y1, 'go', label="Merkle Tree")

    # lower bound plot
    x2 = low_bound_leaves
    y2 = low_bound_hash_calls
    plt.plot(x2, y2, 'bo', label="Lower Bound: Merkle Tree")

    # upper bound plot
    x3 = up_bound_leaves
    y3 = up_bound_hash_calls
    plt.plot(x3, y3, 'co', label="Upper Bound: Merkle Tree")

    # # t5 plot
    # x4 = t5_leaves
    # y4 = t5_hash_calls
    # plt.plot(x4, y4, 'ro', label="T5 Tree")

    # make axes logarithmic
    plt.xscale('log', base=2)
    plt.yscale('log', base=2)

    # labeling the axes
    plt.xlabel('leaves')
    plt.ylabel('# hash calls')

    # add legend
    plt.legend(loc="lower right")

    plt.title(label="Performance Evaluation: Tree Generation")
    plt.grid()
    plt.show()


# NIST parameter: elements in auth.path for each tree concept
# ! aggr, more aggr
def plot_auth_path_length(merkle_leaves: List[int], low_bound_leaves: List[int],
                          up_bound_leaves: List[int], t5_leaves: List[int]):
    pass


if __name__ == '__main__':
    param_set_d = [5, 10, 15, 20, 25]  # height in LMS parameter set for standard Merkle tree
    lower_bound_d = [2, 4, 6, 8, 10]  # height for lower bound t5 trees
    upper_bound_d = [3, 5, 7, 9, 11]  # height for upper bound t5 trees

    # lists of possible leaves for each tree construct,
    # based on LMS param. set
    leaves_list_merkle_standard = power_of_two(param_set_d)
    leaves_list_low_bound = power_of_five(lower_bound_d)
    leaves_list_up_bound = power_of_five(upper_bound_d)

    # ---- hash calls tree generation ----
    # hash calls tree generation: merkle tree
    hash_calls_tree_gen_merkle_tree = merkle_tree_gen_hash_calls(leaves_list_merkle_standard)
    # hash calls tree generation: t5 upper/lower bound tree
    hash_calls_tree_gen_low_bound = t5_tree_gen_hash_calls(leaves_list_low_bound)
    hash_calls_tree_gen_up_bound = t5_tree_gen_hash_calls(leaves_list_up_bound)

    # get int values for hash calls in t5 -> only when leaves are power of 5!
    hash_calls_tree_gen_low_bound = [int(leaves) for leaves in hash_calls_tree_gen_low_bound]
    hash_calls_tree_gen_up_bound = [int(leaves) for leaves in hash_calls_tree_gen_up_bound]

    print('merkle tree: hash calls tree gen.', hash_calls_tree_gen_merkle_tree)
    print('lower bound merkle tree: hash calls tree gen.', hash_calls_tree_gen_low_bound)
    print('upper bound merkle tree: hash calls tree gen.', hash_calls_tree_gen_up_bound)

    # ---- auth.path length ----
    # amount elements in auth.path: merkle tree
    len_auth_path_list_merkle_tree = merkle_tree_len_auth_path_and_verify(leaves_list_merkle_standard)

    # amount elements in auth.path: lower bound / (more) aggressive
    len_auth_path_list_low_aggr = t5_tree_aggr_len_auth_path(leaves_list_low_bound)
    len_auth_path_list_low_more_aggr = t5_tree_more_aggr_len_auth_path(leaves_list_low_bound)

    # amount elements in auth.path: upper bound / (more) aggressive
    len_auth_path_list_up_more_aggr = t5_tree_aggr_len_auth_path(leaves_list_up_bound)
    len_auth_path_list_up_aggr = t5_tree_more_aggr_len_auth_path(leaves_list_up_bound)

    print('merkle tree: length auth.path:', len_auth_path_list_merkle_tree)

    print('lower bound: aggr. length auth.path:', len_auth_path_list_low_aggr)
    print('lower bound: more aggr. length auth.path:', len_auth_path_list_low_more_aggr)

    print('upper bound: aggr. length auth.path:', len_auth_path_list_up_more_aggr)
    print('upper bound: more aggr. length auth.path:', len_auth_path_list_up_aggr)

    # ---- hash calls verify ----
    # Merkle tree: hash calls for path generation / verify
    # for Merkle tree: is same calculation as for length of auth.path
    hash_calls_verify_merkle_tree = len_auth_path_list_merkle_tree

    hash_calls_verify_aggr_low_bound = t5_tree_aggr_verify(leaves_list_low_bound)
    hash_calls_verify_more_aggr_low_bound = t5_tree_more_aggr_verify(leaves_list_low_bound)

    hash_calls_verify_aggr_up_bound = t5_tree_aggr_verify(leaves_list_up_bound)
    hash_calls_verify_more_aggr_up_bound = t5_tree_more_aggr_verify(leaves_list_up_bound)

    print('Merkle tree: hash calls verify', hash_calls_verify_merkle_tree)

    print('lower bound: aggr verify', hash_calls_verify_aggr_low_bound)
    print('lower bound: more aggr verify', hash_calls_verify_more_aggr_low_bound)

    print('upper bound: aggr verify', hash_calls_verify_aggr_up_bound)
    print('upper bound: more aggr verify', hash_calls_verify_more_aggr_up_bound)

    plot_hash_calls_tree_gen(leaves_list_merkle_standard, leaves_list_low_bound,
                             leaves_list_up_bound, hash_calls_tree_gen_merkle_tree,
                             hash_calls_tree_gen_low_bound, hash_calls_tree_gen_up_bound)
