
# If the item is a dummy item, then it will hold the
# position of the dummy variable in the dummy list

class Item:
    
    comp_count = 0 # static variable; counts # of comparisons    
    
    def __init__(self, value, dummy, list_position):
        self.dummy = dummy
        self.value = value
        self.list_position = list_position
        # index of max true value in the subtree of the heap rooted at this node
        self.argmax = -1

    def is_dummy(self):
        return self.dummy

    def get_list_position(self):
        return self.list_position
    
    def update_list_position(self, new_position):
        self.list_position = new_position

    # overload standard operators
    def __eq__(self, other):
        Item.comp_count += 1
        return self.value == other.value

    def __ne__(self, other):
        Item.comp_count += 1
        return self.value != other.value

    def __le__(self, other):
        Item.comp_count += 1
        return self.value <= other.value

    def __ge__(self, other):
        Item.comp_count += 1
        return self.value >= other.value

    def __lt__(self, other):
        Item.comp_count += 1
        return self.value < other.value

    def __gt__(self, other):
        Item.comp_count += 1
        return self.value > other.value

    def __repr__(self):
        return "(" + (str(self.value)+'*' if self.is_dummy() else str(self.value))+", " + str(self.argmax) + ")"
