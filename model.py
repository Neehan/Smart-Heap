import random
from item import Item
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

class Model:
    def __init__(self):
        self.model = RandomForestClassifier()
        self.training = None
        self.X = None
        self.y = None

    def set_train_data(self, data):
        """
        sets training data. 
        if the distribution changes, we might want to change 
        our training data
        """
        self.training = data
    
    def train(self, X, y):
        """
        Given our data, learns the distribution of our data
        """
        self.X = X
        self.y = y
        self.model.fit(X, y)

    def generate(self, n):
        """
        Samples n new points from the learned distribution
        """
        return_list = []
        for i in range(n):
            current_value = random.choice(self.training)
            # dummy variable should hold the position in dummy list
            return_list.append(Item(current_value, True, i))
        return return_list
    
    def predict(self, input):
        return self.model.predict(input)[0] # because the output is a 1d array
        