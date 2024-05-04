"""
One liners are cool, right?
In this program, I have a bunch of algorithms and things implemented using single lines of python code.

Most of these are recursive. To do that, you need a wrapper function and a recursive function. 
The recursive function has to take itself as a parameter, so it has a reference to call itself.
"""

while_loop = lambda prog, cond, state, helper=(lambda prog, cond, state, self: self(prog, cond, prog(state), self) if cond(state) else state): helper(prog, cond, state, helper)

"""
Most of these are coded on multiple lines, then the extra whitespace is removed so that it's one line.
This is standard selection sort, running in O(n^2) time.
"""
selection_sort = lambda arr, key=None, temp=None: (
    [
        (
            key := i,
            [
                key := j if arr[j] < arr[key] else key
                for j in range(i, len(arr))
            ],
            temp := arr[i],
            arr.__setitem__(i, arr[key]),
            arr.__setitem__(key, temp)
        )
        for i in range(len(arr))
    ]
)

"shuffle the list until it's sorted"
bogo_sort = lambda arr: (
    (
        lambda helper, shuffle: helper(shuffle, helper)
    )(
        lambda shuffle, self, temp=None, pos=None: None if all(arr[i] >= arr[i - 1] for i in range(1, len(arr))) else (
            shuffle(),
            self(shuffle, self)
        ),
        lambda: [
            (
                temp := arr[i],
                pos := i + (hash(tuple(arr)) % (len(arr) - i)),
                arr.__setitem__(i, arr[pos]),
                arr.__setitem__(pos, temp)
            )
            for i in range(len(arr))
        ]
        
    )
)

"""
Dump all the items into a min-heap, then take them out in sorted order.
O(n log n)
an entire 1,538 characters when condensed!
"""
heap_sort = lambda arr: (
    (
        lambda heap_insert=None, heap_remove=None, reheap_up=None, reheap_down=None, swap=None, state=[0, [0] * len(arr)]: (
            [heap_insert(state, item, reheap_up, swap) for item in arr],
            [arr.__setitem__(i, heap_remove(state, reheap_down, swap)) for i in range(len(arr))]
        )
    )(

        swap=lambda lst, a, b, temp=None: (
            temp := lst[a],
            lst.__setitem__(a, lst[b]),
            lst.__setitem__(b, temp)
        ),

        heap_insert=lambda state, item, reheap_up, swap, size=None, heap=None: (
            size := state[0],
            heap := state[1],
            heap.__setitem__(size, item),
            reheap_up(heap, size, reheap_up, swap),
            state.__setitem__(0, size + 1)
        ),

        reheap_up=lambda heap, pos, self, swap: (
            None
            if pos == 0 or heap[pos] >= heap[(pos - 1) >> 1]
            else (
                swap(heap, pos, (pos - 1) >> 1),
                self(heap, (pos - 1) >> 1, self, swap)
            )
        ),

        heap_remove=lambda state, reheap_down, swap, size=None, heap=None: (
            size := state[0],
            heap := state[1],
            heap[0],
            state.__setitem__(0, size - 1),
            swap(heap, 0, size - 1),
            reheap_down(state, 0, reheap_down, swap)
        )[2],

        reheap_down=lambda state, pos, self, swap, size=None, heap=None, left_viable=None, right_viable=None, tgt=None: (
            size := state[0],
            heap := state[1],
            left_viable := (pos << 1) + 1 < size and heap[(pos << 1) + 1] < heap[pos],
            right_viable := (pos << 1) + 2 < size and heap[(pos << 1) + 2] < heap[pos],
            (
                tgt := (pos << 1) + 1 if left_viable and (not right_viable or heap[(pos << 1) + 1] < heap[(pos << 1) + 2]) else (pos << 1) + 2,
                swap(heap, pos, tgt),
                self(state, tgt, self, swap)
            ) if left_viable or right_viable else None

        ),
    )
)

"""
Recursively sort the first half, then the second half.
The smallest item is either at the midpoint or the start. Wherever it is, swap it with the start.
Now, the smallest item is in the correct position.
Recursively sort the rest of the list.
"""
slow_sort = lambda arr: (
    (
        lambda swap=None, func=None: (
            swap := lambda a, b, temp=None: (
                temp := arr[a],
                arr.__setitem__(a, arr[b]),
                arr.__setitem__(b, temp),
            ), 
            func := lambda start, stop, self, mid=None: (
                None if stop - start <= 1 else (
                    mid := (start + stop) // 2,
                    self(start, mid, self),
                    self(mid, stop, self),
                    None if arr[start] < arr[mid] else swap(start, mid),
                    self(start + 1, stop, self)
                )
            ),
            func(0, len(arr), func),
            None
        )[-1]
    )()
)

# sorting algorithms, one-line-ified
selection_sort = lambda arr: ((lambda arr, key=None, temp=None: ([(key := i, [key := j if arr[j] < arr[key] else key for j in range(i, len(arr))], temp := arr[i], arr.__setitem__(i, arr[key]), arr.__setitem__(key, temp))for i in range(len(arr))]))(arr), None)[1]
bogo_sort = lambda arr, random=__import__("random", globals(), locals()), loop=lambda prog, cond, state: ([i for i in type("iter", (object,), {"state": state, "__iter__": lambda self: self, "__next__": lambda self: (setattr(self, "state", prog(self.state)) if cond(self.state) else range(0).__iter__().__next__())})()], None)[1]: loop(lambda a: (a, random.shuffle(a))[0], lambda a: any(a[i] < a[i - 1] for i in range(1, len(a))), arr) 
heap_sort = lambda arr: ((lambda heap_insert=None, heap_remove=None, reheap_up=None, reheap_down=None, swap=None, state=[0, [0] * len(arr)]: ([heap_insert(state, item, reheap_up, swap) for item in arr], [arr.__setitem__(i, heap_remove(state, reheap_down, swap)) for i in range(len(arr))], None)[-1])(swap=lambda lst, a, b, temp=None: (temp := lst[a], lst.__setitem__(a, lst[b]), lst.__setitem__(b, temp)), heap_insert=lambda state, item, reheap_up, swap, size=None, heap=None: (size := state[0], heap := state[1], heap.__setitem__(size, item), reheap_up(heap, size, reheap_up, swap), state.__setitem__(0, size + 1)), reheap_up=lambda heap, pos, self, swap: (None if pos == 0 or heap[pos] >= heap[(pos - 1) >> 1] else (swap(heap, pos, (pos - 1) >> 1), self(heap, (pos - 1) >> 1, self, swap))), heap_remove=lambda state, reheap_down, swap, size=None, heap=None: (size := state[0], heap := state[1], heap[0], state.__setitem__(0, size - 1), swap(heap, 0, size - 1), reheap_down(state, 0, reheap_down, swap))[2], reheap_down=lambda state, pos, self, swap, size=None, heap=None, left_viable=None, right_viable=None, tgt=None: (size := state[0], heap := state[1], left_viable := (pos << 1) + 1 < size and heap[(pos << 1) + 1] < heap[pos], right_viable := (pos << 1) + 2 < size and heap[(pos << 1) + 2] < heap[pos], (tgt := (pos << 1) + 1 if left_viable and (not right_viable or heap[(pos << 1) + 1] < heap[(pos << 1) + 2]) else (pos << 1) + 2, swap(heap, pos, tgt), self(state, tgt, self, swap)) if left_viable or right_viable else None)))
slow_sort = lambda arr: ((lambda swap=None, func=None: (swap := lambda a, b, temp=None: (temp := arr[a], arr.__setitem__(a, arr[b]), arr.__setitem__(b, temp), ), func := lambda start, stop, self, mid=None: (None if stop - start <= 1 else (mid := (start + stop) // 2, self(start, mid, self), self(mid, stop, self), None if arr[start] < arr[mid] else swap(start, mid), self(start + 1, stop, self))), func(0, len(arr), func), None)[-1])())


class_from_dict = lambda name, attrs: __build_class__(
    [
        lambda: locals().__setitem__(key, val)
        for key, val in attrs.items()
    ]
)

# avoid hitting the recursion limit while looping, by using type() to create a class object that's an infinite iterator
while_loop = lambda prog, cond, state: (
    [
        i for i in 
        type(
            "iterator_class", 
            (object,), 
            {
                "state": state, 
                "__iter__": lambda self: self,
                "__next__": lambda self: (setattr(self, "state", prog(self.state)) if cond(self.state) else range(0).__iter__().__next__())
            }
        )()
    ],
    None
)[1]

wloop_full = lambda prog, cond, state: ([i for i in type("iter", (object,), {"state": state, "__iter__": lambda self: self, "__next__": lambda self: (setattr(self, "state", prog(self.state)) if cond(self.state) else range(0).__iter__().__next__())})()], None)[1]
wloop_iter = lambda cond: type("while", (object,), {"__iter__": lambda self: self, "__next__": lambda self: None if cond()else range(0).__iter__().__next__()})

lst = [15, 43, 54, 12, 32, 49, 8]
heap_sort(lst)
print(lst)