from distribution_binary_heap import AugmentedBinaryHeap as abh
from model import Model
from item import Item 
from print_heap import printHeapTree
import unittest

class TestTiny(unittest.TestCase):
    def setUp(self):
        """ Load data """
        self.model = Model()
        self.heap = abh(self.model)
        self.heap_sizes = [2, 10, 75, 250, 1177]
        self.N = 1000

    def heap_builder(self, size):
        self.heap.build_heap([i**2 % 100 for i in range(size)])
        for i in range(self.N):
            self.heap.insert(i**2 % 100)   # some random inserts


    def test_doubling(self):
        pass

    def test_heap_property(self):
        for size in self.heap_sizes:
            # build heap of different sizes
            self.heap_builder(size)
            # for every node starting from the root, check the max heap property
            for i in range(1, self.heap.current_size):
                for child in self.heap.children(i):
                    self.assertGreaterEqual(self.heap.heap_list[i], self.heap.heap_list[child])
    
    def test_argmax_notdummy(self):
        for size in self.heap_sizes:
            self.heap_builder(size)
            for i in range(1, self.heap.current_size):
                j = self.heap.heap_list[i].argmax
                if j > -1: self.assertFalse(self.heap.is_dummy(j))

    def test_argmax_correct(self):
        for size in self.heap_sizes:
            # build heap of different sizes
            self.heap_builder(size)
            for i in range(self.heap.current_size-1, 1, -1): # build true argmax from bottom up
                if not self.heap.is_dummy(i):  # non dummy must have same index as argmax
                    self.assertEqual(self.heap.heap_list[i].argmax, i)
                else:
                    child_max = [] # compute argmax from maximum of the children
                    for child in self.heap.children(i):
                        # child's argmax
                        j = self.heap.heap_list[child].argmax
                        # child's maxval
                        if j > -1: child_max.append(self.heap.heap_list[j])
                    if child_max:
                        k = self.heap.heap_list[i].argmax
                        self.assertEqual(self.heap.heap_list[k], max(child_max))


    def test_extract(self):
        for size in self.heap_sizes:
            # build heap of different sizes
            self.heap_builder(size)
            for i in range(1, self.N):
                self.heap.insert((-1)**i*i)   # insert one
                
                a = self.heap.get_max().value # peek max_value with a guaranteed function
                b = self.heap.extract_max().value # check the extracted value
                self.assertEqual(a, b)



if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)