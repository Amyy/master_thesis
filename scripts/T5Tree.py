from __future__ import annotations
import math
from abc import ABC, abstractmethod
from typing import List, Optional


def hash_t5(left_input: int, right_input: int):
    return hash((left_input, right_input))


def xor(left_input: int, right_input: int):
    return left_input ^ right_input


# necessary/pre-step for auth.path calculation
# != auth.path, tree_height = T5Block Tree height, != path calculated by verifier
def calc_t5_path(ot_key_pos: int, tree_height: int):
    path_list = []
    i = ot_key_pos
    for _ in range(tree_height):
        j = i % 5
        path_list.insert(0, j)  # insert in 1st position of list
        i = (i - j) // 5  # relative position in T5 Block
    return path_list  # list: from root to leaf


# path calculated by verifier
def calc_path_verifier(auth_path: List[int], key_pos: int, child_count: int, one_time_signature: int):
    # count hashcalls for authentication
    hash_count = 0

    # calc depth of tree
    tree_depth = int(math.log(child_count, 5))
    path_t5 = calc_t5_path(key_pos, tree_depth)
    last_result = one_time_signature  # later: last_result == output of leaf before

    for index in reversed(path_t5):  # reverse because path calc is bottom to root; index == child pos. in T5 Block
        if index == 0:  # case m1
            m2 = auth_path[-3]
            h2 = auth_path[-2]
            m5 = auth_path[-1]
            h1 = hash_t5(last_result, m2)
            h1_xor = xor(h1, m5)
            h2_xor = xor(h2, m5)
            h3 = hash_t5(h1_xor, h2_xor)
            last_result = xor(h3, m5)  # end result, h3 XOR m5
            auth_path = auth_path[:-3]  # remove already used elements of authpath
            hash_count += 2  # 2 hash calls were used

        elif index == 1:  # case m2
            m1 = auth_path[-3]
            h2 = auth_path[-2]
            m5 = auth_path[-1]
            h1 = hash_t5(m1, last_result)  # last_result == m2
            h1_xor = xor(h1, m5)
            h2_xor = xor(h2, m5)
            h3 = hash_t5(h1_xor, h2_xor)
            last_result = xor(h3, m5)  # end result, h3 XOR m5
            auth_path = auth_path[:-3]  # remove already used elements of authpath
            hash_count += 2  # 2 hash calls were used

        elif index == 2:  # case m3
            m4 = auth_path[-3]
            h1 = auth_path[-2]
            m5 = auth_path[-1]
            h2 = hash_t5(last_result, m4)  # last_result == m3
            h1_xor = xor(h1, m5)
            h2_xor = xor(h2, m5)
            h3 = hash_t5(h1_xor, h2_xor)
            last_result = xor(h3, m5)  # end result, h3 XOR m5
            auth_path = auth_path[:-3]  # remove already used elements of authpath
            hash_count += 2  # 2 hash calls were used

        elif index == 3:  # case m4
            m3 = auth_path[-3]
            h1 = auth_path[-2]
            m5 = auth_path[-1]
            h2 = hash_t5(m3, last_result)  # last_result == m4
            h1_xor = xor(h1, m5)
            h2_xor = xor(h2, m5)
            h3 = hash_t5(h1_xor, h2_xor)
            last_result = xor(h3, m5)  # end result, h3 XOR m5
            auth_path = auth_path[:-3]  # remove already used elements of authpath
            hash_count += 2  # 2 hash calls were used

        elif index == 4:  # case: m5
            # here: last_result == m5
            # other possibility: auth_path[-3] has padding with 0 (to get same authpath length for every case)
            h1 = auth_path[-2]
            h2 = auth_path[-1]
            h1_xor = xor(h1, last_result)
            h2_xor = xor(h2, last_result)
            h3 = hash_t5(h1_xor, h2_xor)
            last_result = xor(h3, last_result)
            auth_path = auth_path[:-2]  # remove already used elements of authpath
            hash_count += 1  # 1 hashcall is used for special case 5

    return last_result, hash_count  # return root, amount of used hash calls


class T5Node(ABC):  # ABC == abstract class
    def __init__(self):
        pass

    @abstractmethod
    def calc_end_hash(self) -> int:
        pass

    @abstractmethod
    def get_hash_count(self) -> int:
        pass

    @abstractmethod
    def calc_auth_path(self, path: List[int]) -> List[int]:
        pass

    @abstractmethod
    def get_child_count(self) -> int:
        pass


class T5Block(T5Node):
    def __init__(self, m1: T5Node, m2: T5Node, m3: T5Node, m4: T5Node, m5: T5Node):
        super().__init__()  # init T5Node class
        self.m1: T5Node = m1
        self.m2: T5Node = m2
        self.m3: T5Node = m3
        self.m4: T5Node = m4
        self.m5: T5Node = m5
        self.h1: Optional[int] = None
        self.h2: Optional[int] = None

    def get_child_count(self) -> int:
        return self.m1.get_child_count() + \
               self.m2.get_child_count() + \
               self.m3.get_child_count() + \
               self.m4.get_child_count() + \
               self.m5.get_child_count()

    def calc_end_hash(self):
        h1 = self.calc_h1()
        h2 = self.calc_h2()
        m5_endhash = self.m5.calc_end_hash()
        h11 = xor(h1, m5_endhash)
        h21 = xor(h2, m5_endhash)

        h3 = hash_t5(h11, h21)
        return xor(h3, m5_endhash)

    def calc_h1(self):
        if self.h1 is None:
            self.h1 = hash_t5(self.m1.calc_end_hash(), self.m2.calc_end_hash())
        return self.h1

    def calc_h2(self):
        if self.h2 is None:
            self.h2 = hash_t5(self.m3.calc_end_hash(), self.m4.calc_end_hash())
        return self.h2

    def get_hash_count(self):  # notably: XOR count == hash count
        return self.m1.get_hash_count() + \
               self.m2.get_hash_count() + \
               self.m3.get_hash_count() + \
               self.m4.get_hash_count() + \
               self.m5.get_hash_count() + 3

    def calc_auth_path(self, path: List[int]) -> List[int]:
        child_pos = path[0]
        remaining_path = path[1:]

        auth_path = []
        if child_pos == 0:  # if "key" = m0
            auth_path.append(self.m2.calc_end_hash())  # value of m2 "before" current node
            auth_path.append(self.calc_h2())
            auth_path.append(self.m5.calc_end_hash())
            auth_path.extend(self.m1.calc_auth_path(remaining_path))  # path[1:] -> give rest of path to subtrees of m0
        elif child_pos == 1:
            auth_path.append(self.m1.calc_end_hash())  # value of m1 "before" current node
            auth_path.append(self.calc_h2())
            auth_path.append(self.m5.calc_end_hash())
            auth_path.extend(self.m2.calc_auth_path(remaining_path))  # path[1:] -> give rest of path to subtrees of m0

        elif child_pos == 2:
            auth_path.append(self.m4.calc_end_hash())
            auth_path.append(self.calc_h1())
            auth_path.append(self.m5.calc_end_hash())
            auth_path.extend(self.m3.calc_auth_path(remaining_path))  # path[1:] -> give rest of path to subtrees of m0

        elif child_pos == 3:
            auth_path.append(self.m3.calc_end_hash())
            auth_path.append(self.calc_h1())
            auth_path.append(self.m5.calc_end_hash())
            auth_path.extend(self.m5.calc_auth_path(remaining_path))  # path[1:] -> give rest of path to subtrees of m0

        elif child_pos == 4:  # special case m5
            # other possibility: add padding with 0 here to get same authpath len for every case
            auth_path.append(self.calc_h1())
            auth_path.append(self.calc_h2())
            auth_path.extend(self.m5.calc_auth_path(remaining_path))  # path[1:] -> give rest of path to subtrees of m0

        return auth_path


class T5Leaf(T5Node):
    def __init__(self, leaf: int):
        super().__init__()
        self.leaf: int = leaf

    def calc_end_hash(self):
        return self.leaf

    def get_hash_count(self) -> int:  # leaf does not have previous hash calls
        return 0

    def calc_auth_path(self, path: List[int]) -> List[int]:
        return []

    def get_child_count(self) -> int:
        return 1


if __name__ == '__main__':
    s = 22  # leaf position of one-time key used by the signer
    one_time_key = 22  # value of one-time key (here: has same value as position it's on, for debugging purposes)

    path = calc_t5_path(s, 2)
    print('t5_path "T5 layers":', path)

    # Amount T5Leafs -> has to be power of 5, values of leaves == value of one-time public key
    t5tree = T5Block(
        T5Block(T5Leaf(0), T5Leaf(1), T5Leaf(2), T5Leaf(3), T5Leaf(4)),
        T5Block(T5Leaf(5), T5Leaf(6), T5Leaf(7), T5Leaf(8), T5Leaf(9)),
        T5Block(T5Leaf(10), T5Leaf(11), T5Leaf(12), T5Leaf(13), T5Leaf(14)),
        T5Block(T5Leaf(15), T5Leaf(16), T5Leaf(17), T5Leaf(18), T5Leaf(19)),
        T5Block(T5Leaf(20), T5Leaf(21), T5Leaf(22), T5Leaf(23), T5Leaf(24))
    )

    child_count = t5tree.get_child_count()
    print('Amount of leaves', child_count)

    print('Hash of root == public key:', t5tree.calc_end_hash())  # public key Y from signer

    print('# hash calls keygen / T5 tree generation:', t5tree.get_hash_count())

    # signer uses already constructed path -> no new hashcalls necessary
    auth_path = t5tree.calc_auth_path(path)
    print('Auth. path (calculated by signer):', auth_path)

    auth_path_by_verifier, hash_count_authentication = calc_path_verifier(auth_path, s, child_count, one_time_key)
    print('Root calculated by verifier using Authentication path:', auth_path_by_verifier)
    print('# hash calls verification (Path calculation by verifier):', hash_count_authentication)
