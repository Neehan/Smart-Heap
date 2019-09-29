"""
Adib Hasan, Angelos Pelecanos
This code is part of a project for the class
6.890 - Learning-Augmented Algorithms
Spring 2019
"""

from item import Item
from model import Model
from dummy_list import DummyList
from math import ceil, log
from print_heap import printHeapTree


class AugmentedBinaryHeap:
    def __init__(self, model_function):
        """
        Initialization Function
        """
        self.heap_list = [None]         # list of items
        self.current_size = 0           
        self.model = model_function     # model used to predict
        self.dummy_list = None          # this will save the dummy list

    
    #######################################################################################################
    # Regular Heap Functions (Augmented)
    #######################################################################################################

    def build_heap(self, element_list):
        """
        Builds a Max Heap out of element_list. 
        Takes linear time
        Also samples extra n dummy values
        """
        
        item_list = self.itemize_elements(element_list)  # convert every element into an Item object
        self.model.set_train_data(element_list)       # models will be trained on this data
        self.heap_list = [None] + item_list
        self.current_size = len(self.heap_list)       # initialize size correctly        
        self.resize_heap()                            # add dummies to the heap
        


    def resize_heap(self):
        """`
        adds n new dummies to the bottom of the heap in O(n) time
        """
        # print('Rebuilding Heap...')
        true_size = self.count_nondummy()           # count non-dummy (true) values in the heap
        dummy_size = self.current_size - true_size - 1  # number of existing dummies
        dummy_values = self.model.generate(true_size - dummy_size) # samples remaining dummies

        self.dummy_list = None                      # this dummy list is no longer valid
                                                    # heap has 2 * true size elements now
        self.heap_list += dummy_values              # add the dummy values
        self.current_size = len(self.heap_list)     # initialize size correctly


        # build heap 
        n = true_size
        while (n > 0):                              # heapify the elements one by one
            self.swap_down(n)
            n = n - 1
        self.initialize_dummy_list()
        
        X, y = self.get_training_samples()          # train model on these training samples
        self.model.train(X, y)

    

    def swap_up(self, i):
        """
        Swapping Up Function
        Given the index of an element in the list, it swaps it up until it satisfies the heap property
        """
        i_prev = i # position before swap
        while i // 2 > 0:
            if self.heap_list[i] > self.heap_list[i // 2]:  # if the element is smaller than its parent
                self.swap(i, i // 2)
                i = i // 2      # update position of current element
            else: # else the element does satisfy heap property and we are done
                break

        self.update_ancestors_argmax(i_prev, i)  # update argmax of the ancestors

    def swap_down(self, i):
        """
        Swapping Down Function
        Given the index of an element in the list, it swaps it down 
        until it satisfies the heap property
        """
        i_prev = i
        while (i * 2) < self.current_size:
            child = self.max_child(i)
            if self.heap_list[i] < self.heap_list[child]:   # if the element is greater than its child
                self.swap(i, child) # swap values at index i and child
                i = child   # update position of current element
            else: # else element does satisfy heap property and we are done
                break
        self.update_ancestors_argmax(i, i_prev)  # update argmax of the ancestors



    def insert(self, k):
        """
        Insertion Function
        Given a new element, predict the index of the dummy value in the dummy value list
        Insert at that index and propagate up and down as needed
        """
        dummy_index = self.model.predict([[k]])                         # get the index of the dummy value
        target_index = self.dummy_list.get_next_dummy(dummy_index)  # get the index of an empty dummy
        if target_index is not None:
            self.heap_list[target_index].value = k
            self.heap_list[target_index].dummy = False
            self.heap_list[target_index].argmax = target_index
            self.swap_up(target_index)                  # try swapping up
            self.swap_down(target_index)                # try swapping down (will not do anything if it has moved)
        else:
            self.resize_heap()
            self.insert(k)

    def get_max(self, node=1):
        """
        Get maximum value while avoiding dummies
        """
        argmax = self.heap_list[node].argmax
        if argmax > -1:
            return self.heap_list[argmax]

    def extract_max(self):
        """
        Extract Maximum Function
        Returns and deletes the maximum element from the heap
        """
        if self.current_size == 1: return None          # heap is empty
        retval = self.heap_list[1].argmax               # maximum element is at index 1
        if self.is_dummy(retval):
            raise ValueError("A dummy is being extracted.")
        if retval > -1:                                 # argmax is valid 
            self.swap(retval, self.current_size - 1)    # move last element to the top
            self.current_size = self.current_size - 1   # decrease size
            maxval = self.heap_list[-1]
            self.heap_list.pop()                        # delete last element
            
            self.update_ancestors_argmax(self.current_size // 2, self.current_size // 2)
            if retval != self.current_size:
                self.swap_down(retval)                    # swap down top element
                self.swap_up(retval)                    # swap down top element
            return maxval






    #######################################################################################################
    # Helper Functions
    #######################################################################################################


    def count_nondummy(self):
        """
        count the number of non-dummies in the heap
        """
        count = 0
        for i in range(1, self.current_size):
            if not self.is_dummy(i): count += 1
        return count

    
    def itemize_elements(self, element_list):
        """
        Given a list of elements, create a list of non-dummy elements
        """
        item_list = []
        for element in element_list:
            item_list.append(Item(element, False, -1))
            item_list[-1].argmax = len(item_list) - 1 # for a true value argmax is its index in the heap
        return item_list

    
    def initialize_dummy_list(self):
        """
        This function is called after the building to set up the dummy list
        """
        dummy_positions = []                    # the index that the dummy value is
        for i in range(1, self.current_size):   # check all values if they are dummy
            if self.is_dummy(i):
                dummy_positions.append(i)
                # a dummy element should remember its position in dummy list
                self.heap_list[i].update_list_position(len(dummy_positions)-1)
        self.dummy_list = DummyList(dummy_positions)

    
    def get_training_samples(self):
        """
        training sample is (dummy value --> its index in the dummy list)
        """
        X = [] # input
        y = [] # label
        # for heap position of each dummy
        for pos in self.dummy_list.heap_position:
            X.append([self.heap_list[pos].value])
            y.append(self.heap_list[pos].get_list_position())
        return X, y


    def is_dummy(self, i):
        """
        Is the item at index i dummy?
        """
        return self.heap_list[i].is_dummy()

    

    def children(self, i):
        """
        Given the index of an element, returns the indices of 
        its children as a list. If there is no child, returns an empty list
        """
        if i * 2 >= self.current_size:
            return []
        elif i * 2 + 1 >= self.current_size:
            return [i * 2]
        else:
            return [i * 2, i * 2 + 1]


    def max_child(self, i):
        """
        Given the index of an element, returns the index of 
        its max_child
        """
        if i * 2 + 1 >= self.current_size:
            return i * 2
        else:
            if self.heap_list[i*2] > self.heap_list[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1


    def get_children_argmax(self, i):
        """
        argmax-es over the children of node i 
        """

        argmax = -1
        for child in self.children(i):
            if child < 0 or child >= self.current_size:
                raise ValueError("invalid child")
            j = self.heap_list[child].argmax if self.is_dummy(child) else child # subtree max of child
            if j >= self.current_size:
                raise ValueError("invalid argmax")
            if j > -1:                         # this child has valid argmax
                if argmax <= -1: argmax = j    # current argmax is invalid, so set current argmax
                elif self.heap_list[j] > self.heap_list[argmax]: argmax = j # j has better argmax
        return argmax


    def update_ancestors_argmax(self, i, j):
        """
        given the index of a non-dummy node, it updates argmax of all its ancestors 
        until it finds a nondummy node
        starts from node i, always goes up to ancestor j, then stops first time it finds
        two ancestor sharing same argmax
        """
        while i > 0:
            if self.heap_list[i].is_dummy():
                parent_argmax = self.heap_list[i].argmax
                child_argmax = self.get_children_argmax(i) # best argmax among all children
                if child_argmax != parent_argmax: # parent is dummy, so must have same as best child's argmax
                    self.heap_list[i].argmax = child_argmax
                elif i < j:# parent, child have same argmax and checked upto ancestor j
                    break # no point looking above parent
            else: # parent is a non dummy value
                self.heap_list[i].argmax = i
            i = i // 2      # update position of current element



    def swap(self, i, j):
        """
        swaps values of node i and j in the heap
        """
        # swaps values at i and j
        item_i = self.heap_list[i]
        item_j = self.heap_list[j]

        if self.dummy_list is not None:
            if item_i.is_dummy():
                # item_i is going to position j, so update that in the dummy list
                self.dummy_list.update_heap_position(item_i.get_list_position(), j)

            if item_j.is_dummy():
                # item_j is going to position i, so update that in the dummy list
                self.dummy_list.update_heap_position(item_j.get_list_position(), i)
        
        # swap values
        self.heap_list[i], self.heap_list[j] = item_j, item_i


