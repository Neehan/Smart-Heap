from distribution_binary_heap import AugmentedBinaryHeap as abh
from original_binary_heap import BinaryHeap as bh
from model import Model
import item
from math import log
from print_heap import printHeapTree
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier


x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
y = []
z = []

for i in x:
    print(i)
    print("Starting abh...")
    N = 2**i
    # augmented heap
    item.Item.comp_count = 0
    model = Model()
    heap = abh(model)
    heap.build_heap([(-1)**j*(j**2 % 10) for j in range(100)])
    for j in range(1, N):
        if j == N//3:
            print("1/3 insert completed...")
        if j == 2 * N//3:
            print("2/3 insert completed...")
        heap.insert((-1)**(j**2 % 11))
        heap.extract_max().value
    y.append(log(item.Item.comp_count))

    # regular heap
    item.Item.comp_count = 0
    heap = bh()
    print("Starting bh...")
    heap.build_heap([(-1)**j*(j**2 % 10) for j in range(100)])
    for j in range(1, N):
        if j == N//3:
            print("1/3 insert completed...")
        if j == 2 * N//3:
            print("2/3 insert completed...")
        heap.insert((-1)**(j**2 % 11))
        heap.extract_max().value
    z.append(log(item.Item.comp_count))


a = pd.DataFrame({'log n' : x, 'log comparison' : y})
b = pd.DataFrame({'log n' : x, 'log comparison' : z})
c = pd.concat([a.assign(dataset='augmented bh'), b.assign(dataset='original bh')])
print(c)
sns.scatterplot(x='log n', y='log comparison', data=c,
                style='dataset')
plt.show()