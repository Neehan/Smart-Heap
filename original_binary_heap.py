"""
Adib Hasan, Angelos Pelecanos
This code is part of a project for the class
6.890 - Learning-Augmented Algorithms
Spring 2019
"""
from item import Item


class BinaryHeap: # MinBinaryHeap
    def __init__(self):
        """
        Initialization Function
        """
        self.heap_list = [None]
        self.current_size = 0


    def swap_up(self, i):
        """
        Swapping Up Function
        Given the index of an element in the list, it swaps it up until it satisfies the heap property
        """
        while i // 2 > 0:
            if self.heap_list[i] > self.heap_list[i // 2]: # if the element is smaller than its parent
                self.heap_list[i // 2], self.heap_list[i] = self.heap_list[i], self.heap_list[i // 2]   # swap with the parent
                i = i // 2                                                                              # update position of new element
            else: # else the element does satisfy heap property and we are done
                break

    def insert(self, k):
        """
        Insertion Function
        Given a new element, insert it to the bottom of the heap and propagate as needed
        """
        self.heap_list.append(Item(k, False, -1))
        self.current_size += 1
        self.swap_up(self.current_size)

    def swap_down(self, i):
        """
        Swapping Down Function
        Given the index of an element in the list, it swaps it down until it satisfies the heap property
        """
        while (i * 2) <= self.current_size:
            child = self.max_child(i)
            if self.heap_list[i] < self.heap_list[child]: # if the element is greater than its child
                self.heap_list[i], self.heap_list[child] = self.heap_list[child], self.heap_list[i] # swap with the child
                i = child                                                                           # update position of new element
            else: # else element does satisfy heap property and we are done
                break

    def max_child(self, i):
        """
        Maximum Child Function
        Given the index of an element, returns the index of the child with maximum value
        """
        if i * 2 + 1 > self.current_size:
            return i * 2
        else:
            if self.heap_list[i*2] > self.heap_list[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1

    def get_max(self):
        return self.heap_list[1]

    def extract_max(self):
        """
        Extract Maximum Function
        Returns and deletes the maximum element from the heap
        """
        retval = self.heap_list[1]                              # maximum element is at index 1
        self.heap_list[1] = self.heap_list[self.current_size]   # move last element to the top
        self.current_size = self.current_size - 1               # decrease size
        self.heap_list.pop()                                    # delete last element
        self.swap_down(1)                                       # swap down top element
        return retval

    
    def itemize_elements(self, element_list):
        """
        Given a list of elements, create a list of non-dummy elements
        """
        item_list = []
        for element in element_list:
            item_list.append(Item(element, False, -1))
            item_list[-1].argmax = len(item_list) - 1 # for a true value argmax is its index in the heap
        return item_list


    def build_heap(self, element_list):
        item_list = self.itemize_elements(element_list)  # convert every element into an Item object
        i = len(item_list) // 2              # get middle element of list
        self.current_size = len(item_list)   # initialize size correctly
        self.heap_list = [0] + item_list[:]  # initialize list 
        while (i > 0):                          # heapify the elements one by one
            self.swap_down(i)
            i = i - 1
