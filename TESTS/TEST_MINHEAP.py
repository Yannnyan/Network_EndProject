import unittest
from Algorithms import Minheap


class minheap1(unittest.TestCase):
    def test_minheap(self):
        heap = Minheap.MinHeap()
        l1 = [9, 2, 5, 8, 4, 5, 0, 1]
        l2 = [0, 1, 2, 3, 4, 5, 6, 7]
        l3 = []
        for i in range(len(l1)):
            l3.append((l1[i], l2[i]))
        for i in range(len(l3)):
            heap.insert(l3[i][0], l3[i][1])
        print(heap.heap)
        heap.DecreaseKey(2, 1)
        print(heap.heap)
