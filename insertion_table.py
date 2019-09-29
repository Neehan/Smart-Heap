from model import Model
from dummy_list import DummyList

class InsertionTable(object):
    """
    Insertion Table implementation for priority queues.
    This class maintains a sorted list as data structure 
    at all times. It also has a list of dummy values that
    are assumed to be predicted future insertions to the
    list. If the prediction is correct, the cost for
    an insertion is O(1).
    """
    def __init__(self):
        self.table = []
        self.dummies = []

    def resize_table(self):
        self.dummies = model.generate(len(table) + 1)
        self.dummies.sort()
        self.merge(self.table, self.dummies)
        # give dummy list to model?
        model.train(dummies)

    def merge(self, table, dummies):
        i = j = k = 0
        self.table = []
        # Copy data from previous table and new 
        # dummy list to table, but avoid duplicates
        # from dummy list 
        
        while i < len(table) and j < len(dummies): 
            if table[i] < dummies[j]: 
                self.table[k] = table[i] 
                i += 1
            # this dummy is not in table
            elif dummies[j].index() is None: 
                self.table[k] = dummies[j] 
                j += 1
            k += 1
          
        # Checking if any element was left 
        while i < len(table): 
            self.table[k] = L[i] 
            i += 1
            k += 1
          
        while j < len(dummies): 
            if dummies[j].index() is None:
                self.table[k] = dummies[j] 
                j += 1
                k += 1


    def swap_sort(self, i):
        """
        i = index of self.table
        given the unsorted index in an otherwise sorted list
        swaps the value at unsorted index left or right
        until the list is sorted
        """
        table = self.table
        if i < 0 or i >= len(table):
            raise ValueError("list index out of range")
        if i > 0:
            # swap left
            if table[i] < table[i-1]:
                table[i], table[i-1] = table[i-1], table[i]
                self.swap_sort(i-1)
        elif i < len(table)-1:
            # swap right
            if table[i] > table[i+1]:
                table[i], table[i+1] = table[i+1], table[i]
                self.swap_sort(i+1)
        # else: the list has just one element
        # it's already sorted. do nothing

    def insert(val):
        """
        val = a value of type Object
        insert it into self.table. replace a dummy (place holder)
        value, and swap until the list is sorted again
        """
        table = self.table
        # model predicts index of the val in the dummies
        i = model.predict(val)
        
        # invalid index; find any dummy
        if 0 < i or i >= len(table): i = 0
        
        # dummy at index i might be occupied by an earlier
        # insertion. so, get index of the next empty dummy
        # in the dummy list
        dummy_idx = self.dummies.get_next_dummy(i)
        
        # no empty dummy left
        if dummy_idx is None:
            # need to generate new dummies
            self.resize_table()
            self.insert(val)
        
        # index of the empty dummy in the table
        idx = self.dummies[dummy_idx].index()
        # insert val into table
        table[idx] = val

        # mark this dummy filled in the dummy list
        self.dummies.fill_in_dummy(dummy_idx)

        
        # the table can become unsorted because of this
        # insertion. so, swap this value until table is sorted
        self.swap_sort(idx)


    def extract_max():
        """
        extract maximum element of the table. the table is sorted
        so, it's the last element
        """
        max_elt = self.table[-1]
        del self.table[-1]
        return max_elt
