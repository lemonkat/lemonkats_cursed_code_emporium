# A couple classes that implement dictionaries in sub-optimal ways.

import random

class LogDictionary:
    """
    The LogDictionary!
    This dictionary implementation has O(1) insert and remove, at the cost of O(n) lookup.
    It has the advantage over traditional hash table methods in that it can be copied in O(1) time.

    It works by simply keeping a log of all insertions and deletions that have happened to it. 
    To look up a key, we just go back through our log until we find the most recent action involving our key.
    If we reach the end of the log, we return None.
    We use a linked list to store the log, inserting at the head, so a copy of the LogDict can point to the same linked list with no problems.
    This allows for the O(1) copy.
    """
    def __init__(self, items: list[tuple[object, object]] = None) -> None:
        self.data = None
        self.len = 0
        if items:
            for key, val in items:
                self[key] = val

    def __contains__(self, key: object) -> bool:
        return self[key] is not None

    def __setitem__(self, key: object, val: object) -> None:
        self.data = key, val, self.data

    def __getitem__(self, key: object) -> object:
        node = self.data
        while node:
            k, v, n = node
            if k == key:
                return v
            node = n
        return None

    def __len__(self) -> int:
        keys = []
        node = self.data
        while node:
            k, v, n = node
            if k not in keys:
                keys.append(k)
            node = n
        return len(keys)
    
class HashTree:
    """
    A hybrid between a tree-based dictionary and a hash-table based dictionary.
    Imagine a hash table that uses buckets to handle collisions, but the buckets are hash tables.
    The table sizes follow the fibonacci sequence.
    """
    def __init__(self, items: list[tuple[object, object]] = None, table_size: int = 5, next_table_size: int = 8) -> None:
        self._data = None
        self._table_size, self._next_table_size = table_size, next_table_size
        if items:
            for key, val in items:
                self[key] = val
    
    def __len__(self) -> int:
        if self._data is None:
            return 0
        if isinstance(self._data, list):
            return sum(map(len, self._data))
        else:
            return 1
    
    def __contains__(self, key: object) -> bool:
        return self[key] is not None

    def __getitem__(self, key: object) -> object:
        if self._data is None:
            return None
        
        elif isinstance(self._data, list):
            return self._data[hash(key) % self._table_size][key]
        
        elif self._data[0] == key:
            return self._data[1]
        
        else:
            return None

    def __setitem__(self, key: object, val: object) -> None:        
        if self._data is None:
            self._data = key, val
        
        elif isinstance(self._data, list):
            self._data[hash(key) % self._table_size][key] = val
        
        elif self._data[0] == key:
            self._data = key, val
        
        else:
            old_key, old_val = self._data
            self._data = [
                HashTree(
                    table_size=self._next_table_size, 
                    next_table_size=self._table_size + self._next_table_size
                )
                for _ in range(self._table_size)
            ]
            self[old_key] = old_val
            self[key] = val
            


class BogoHashTree:
    """
    And now, an even worse version of the HashTree: The BogoHashTree!
    It's like the hash tree, but the 'hash function' is a random number generator.
    So the data structure kinda just searches randomly through its absolute mess of a tree structure
    until it finds what it's looking for.
    """
    # single key-value pair
    class Node:
        def __init__(self, key: object, value: object) -> None:
            self.key = key
            self.value = value

        def __len__(self) -> int:
            return 1

        def __contains__(self, key: object) -> bool:
            return key == self.key

        def __getitem__(self, key: object) -> object:
            return self.value if self.key == key else None

        def __setitem__(self, key: object, value: object) -> None:
            if key == self.key:
                self.value = value

        def convert(self, m: int) -> "BogoHashTree":
            result = BogoHashTree(m)
            result[self.key] = self.value
            return result
        
    def __init__(self, m: int = 8) -> None:
        self.data = [None] * m
        self.m = m

    # randomly pick indices and look there
    # if we've gone through all of them, doesn't exist
    def _find_idx(self, key: object) -> int:
        remaining = [True] * self.m
        while sum(remaining):
            idx = random.randint(0, self.m - 1)
            if self.data[idx] and key in self.data[idx]:
                return idx
            remaining[idx] = False
        return -1

    # it could be stored, but meh
    def __len__(self) -> int:
        return sum(len(item) for item in self.data if item)

    def __contains__(self, key: object) -> bool:
        return self._find_idx(key) != -1

    def __getitem__(self, key: object) -> object:
        idx = self._find_idx(key)
        if idx == -1:
            return None
        return self.data[idx][key]

    def __setitem__(self, key: object, value: object) -> None:
        idx = self._find_idx(key)
        # we don't have an entry yet
        if idx == -1:
            idx = random.randint(0, self.m - 1)
            # something already at the idx we want
            if self.data[idx]:
                # convert single-element node to tree
                # might give a few false positives, but its prob fine
                if len(self.data[idx]) == 1:
                    self.data[idx] = self.data[idx].convert(self.m)
                self.data[idx][key] = value
            # just toss it there
            else:
                self.data[idx] = BogoHashTree.Node(key, value)
        # we already have an entry, edit it
        else:
            self.data[idx][key] = value



if __name__ == "__main__":
    test = BogoHashTree()
    ref = {}

    for i in range(1000):
        match random.choice(["get", "set", "len"]):
            case "get":
                key = random.randint(1, 100)
                if key in ref:
                    assert test[key] == ref[key]
            case "set":
                key = random.randint(1, 100)
                val = random.randint(1, 100)
                test[key] = val
                ref[key] = val
            case "len":
                assert len(test) == len(ref), (test, ref)
