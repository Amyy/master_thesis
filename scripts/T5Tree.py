from __future__ import annotations

from abc import ABC, abstractmethod


def hash_t5(left_input: int, right_input: int):
    return hash((left_input, right_input))


def xor(left_input: int, right_input: int):
    return left_input ^ right_input


# != authpath, tree_height = T5Block Tree height
def calc_path(ot_key_pos: int, tree_height: int):
    path_list = []
    i = ot_key_pos
    for _ in range(tree_height):
        j = i % 5
        path_list.insert(0, j)  # 1st position of list
        i = (i - j) // 5  # relative position in T5 Block
    return path_list  # list: from root to leaf


class T5Node(ABC):  # ABC == abstract class
    def __init__(self):
        pass

    @abstractmethod
    def calc_end_hash(self) -> int:
        pass

    @abstractmethod
    def get_hash_count(self) -> int:
        pass


class T5Block(T5Node):
    def __init__(self, m1: T5Node, m2: T5Node, m3: T5Node, m4: T5Node, m5: T5Node):
        super().__init__()  # init T5Node class
        self.m1: T5Node = m1
        self.m2: T5Node = m2
        self.m3: T5Node = m3
        self.m4: T5Node = m4
        self.m5: T5Node = m5

    def calc_end_hash(self):
        h1 = hash_t5(self.m1.calc_end_hash(), self.m2.calc_end_hash())
        h2 = hash_t5(self.m3.calc_end_hash(), self.m4.calc_end_hash())
        m5_endhash = self.m5.calc_end_hash()
        h11 = xor(h1, m5_endhash)
        h21 = xor(h2, m5_endhash)

        h3 = hash_t5(h11, h21)
        return xor(h3, m5_endhash)

    def get_hash_count(self):  # notably: XOR count == hash count
        return self.m1.get_hash_count() + \
               self.m2.get_hash_count() + \
               self.m3.get_hash_count() + \
               self.m4.get_hash_count() + \
               self.m5.get_hash_count() + 3


class T5Leaf(T5Node):
    def __init__(self, leaf: int):
        super().__init__()
        self.leaf: int = leaf

    def calc_end_hash(self):
        return self.leaf

    def get_hash_count(self) -> int:  # leaf does not have previous hash calls
        return 0


if __name__ == '__main__':

    print(calc_path(113,3))

    quit()
    # Amount T5Leafs -> has to be power of 5
    t5tree = T5Block(
        T5Block(T5Leaf(1), T5Leaf(2), T5Leaf(3), T5Leaf(4), T5Leaf(5)),
        T5Block(T5Leaf(6), T5Leaf(7), T5Leaf(8), T5Leaf(9), T5Leaf(10)),
        T5Block(T5Leaf(11), T5Leaf(12), T5Leaf(13), T5Leaf(14), T5Leaf(15)),
        T5Block(T5Leaf(16), T5Leaf(17), T5Leaf(18), T5Leaf(19), T5Leaf(20)),
        T5Block(T5Leaf(21), T5Leaf(22), T5Leaf(23), T5Leaf(24), T5Leaf(25))
    )
    print(t5tree.calc_end_hash())
    print('hashcount: ', t5tree.get_hash_count())
