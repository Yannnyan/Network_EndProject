# class from oop project Ex3 github Yannnyan/Uni-Ariel-OOPEx3

class MinHeap:
    """This Class Implements the Min Heap Data set,
    Its specialty is that it Implements Decrease Key with runtime O(log n)"""

    def __init__(self):
        # heap containing tuple (weight, nodeId)
        self.heap = []
        # the first value in the heap at index 0 is None
        self.heap.append(None)
        # dictionary maps id(a.k.a key) to index (a.k.a value) inside the heap
        self.keyToIndex = {}

    def size(self) -> int:
        return len(self.heap)

    def swim(self, IdNode):
        """
        Heapify Up function, O(log n)
        :param IdNode: The id of the node which should be Heapified
        """
        indexOfNode = self.keyToIndex[IdNode]
        if indexOfNode == 1:
            return
        parentIndex = int(indexOfNode / 2)
        if self.heap[parentIndex][0] > self.heap[indexOfNode][0]:
            self.swap(self.heap[parentIndex][1], IdNode)
            self.swim(self.heap[parentIndex][1])

    def sink(self, parentId):
        """
        Heapify Down function, O(log n)
        :param parentId: The id of the node which should be Heapified
        """
        parentIndex = self.keyToIndex.get(parentId)
        if parentIndex >= self.size():
            return
        leftChildIndex = parentIndex * 2
        rightChildIndex = parentIndex * 2 + 1
        if leftChildIndex >= self.size():
            return
        # parent bigger than left child and right not exist, swap and call sink
        elif rightChildIndex >= self.size():
            if self.heap[leftChildIndex][0] < self.heap[parentIndex][0]:
                self.swap(self.heap[leftChildIndex][1], self.heap[parentIndex][1])
                self.sink(leftChildIndex)
        # parent bigger than the minimal of right and left, swap them and call recursivly
        else:
            # take child with minimal weight
            minimumChild = leftChildIndex if self.heap[leftChildIndex][0] < self.heap[rightChildIndex][
                0] else rightChildIndex
            if self.heap[minimumChild][0] < self.heap[parentIndex][0]:
                self.swap(self.heap[minimumChild][1], self.heap[parentIndex][1])
                self.sink(self.heap[minimumChild][1])

    def insert(self, weight, nodeId):
        """
        Inserts a new object into the Min heap O(log n)
        :param weight: the weight of the Node, by which we place the node in the Heap
        :param nodeId: the id of the Node the user wants to add to the heap
        """
        if weight is None or nodeId is None:
            raise RuntimeWarning("Cant add null to heap")
        self.heap.append((weight, nodeId))
        self.keyToIndex[nodeId] = self.size() - 1
        self.swim(nodeId)

    def removeMin(self) -> int:
        """
        Removes and Return the smallest object (By weight) in the Heap, O(log n)
        :return: int - the id of the node with the smallest weight
        """
        if self.size() == 2:
            minimalNode = self.heap.pop(1)
            return minimalNode[1]
        self.swap(self.heap[1][1], self.heap[(self.size() - 1)][1])
        minimalNode = self.heap.pop(self.size() - 1)
        self.sink(self.heap[1][1])
        return minimalNode[1]

    def remove(self, nodeId):
        index = self.keyToIndex[nodeId]
        self.swap(self.heap[index][1], self.heap[(len(self.heap) - 1)][1])
        resNodeId = self.heap.pop(self.size() - 1)[1]
        self.sink(resNodeId)
        return resNodeId

    def isEmpty(self):
        """
        :return: bool - True if the Heap is empty, False if it isn't
        """
        return self.size() == 1

    def DecreaseKey(self, NodeId, weight):
        """
        Decreases the key of the given node, by the given weight,
        will change it's place in the Heap approximately. O(log n)
        :param NodeId: Id of the Node whose weight the user want's to change
        :param weight: The new Weight of the given Node
        """
        try:
            nodeIndex = self.keyToIndex.get(NodeId)
            if nodeIndex > len(self.heap):
                return
            if weight < self.heap[nodeIndex][0]:
                self.heap.pop(nodeIndex)
                self.heap.insert(nodeIndex, (weight, NodeId))
                self.swim(NodeId)
        except KeyError:
            print("Node Id inserted at DecreaseKey Does not exist!")

    def swap(self, iId, jId):
        """ An auxiliary function that swaps to nodes in the Heap"""
        # swaps the indexes respectively to their location
        iIndex = self.keyToIndex[iId]
        jIndex = self.keyToIndex[jId]
        self.heap[iIndex], self.heap[jIndex] = self.heap[jIndex], self.heap[iIndex]
        self.keyToIndex[iId] = jIndex
        self.keyToIndex[jId] = iIndex
