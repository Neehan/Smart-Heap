
# Inspired from Union-Find

class DummyList:
    def __init__(self, heap_position):
        self.size = len(heap_position)
        self.heap_position = heap_position # dummy[i] will be in position of i-th dummy in the heap
        self.pre = [i for i in range(self.size)]
        self.rank = [0 for i in range(self.size)]
        self.next_value = [i for i in range(self.size)]

    def find_pre(self, x):
        if self.pre[x] != x:
            self.pre[x] = self.find_pre(self.pre[x])
            return self.pre[x]
        return x

    def get_next_dummy(self, x):
        parent = self.find_pre(x)
        next_dummy_index = self.next_value[parent]
        if self.unset_dummy(next_dummy_index): # unset was successful
            return self.heap_position[next_dummy_index]
        else: return None # no dummy left

    def unset_dummy(self, x): # union x with x+1 
        return self.union(x, (x+1)%self.size) # return whether the union was successful

    def update_heap_position(self, idx, new_position):
        # needed for when we swap with dummy values to change where they point in the heap
        self.heap_position[idx] = new_position

    #####################################################
    # Internal Functions
    #####################################################

    def union(self, x, y): # union x and y
        px = self.find_pre(x)
        py = self.find_pre(y)
        correct_next_value = self.next_value[py]

        if px == py:
            return False # we have filled our dummy values, union unsuccessful
        
        if self.rank[px] > self.rank[py]:
            self.pre[py] = px
            self.next_value[px] = correct_next_value
        else:
            self.pre[px] = py
        if self.rank[px] == self.rank[py]:
            self.rank[py] += 1

        return True # union successful
