from random import shuffle
from ID3 import *
from operator import xor
from parse import parse
from parse2 import parse2
from copy import deepcopy
import matplotlib.pyplot as plt
import os.path
from pruning import validation_accuracy

# NOTE: these functions are just for your reference, you will NOT be graded on their output
# so you can feel free to implement them as you choose, or not implement them at all if you want
# to use an entirely different method for graphing

def get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, pct):
    '''
    get_graph_accuracy_partial - Given a training set, attribute metadata, validation set, numerical splits count, and percentage,
    this function will return the validation accuracy of a specified (percentage) portion of the trainging setself.
    '''
    aver = 0
    for i in range(0,iterations):
        shuffle(train_set)
        temppart = []
        for j in range(0, int(len(train_set) * pct2)):# pick part of the training set
            temppart.append(train_set[j])
        numerical_splits_count1 = deepcopy(numerical_splits_count)
        depth1 = deepcopy(depth)
        tree = ID3(temppart, attribute_metadata, numerical_splits_count1, depth1)# train 
        accuracy = validation_accuracy(tree,validate_set)
        aver = aver + accuracy
    aver = aver / iterations# calculate the average accuracy for a certain pct
    return aver

def get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations):
    '''
    Given a training set, attribute metadata, validation set, numerical splits count, iterations, and percentages,
    this function will return an array of the averaged graph accuracy partials based off the number of iterations.
    '''
    array = []
    for pct in range(1, 11):
        pct = float(pct) / 10 # percentage = 0.1, 0.2, ... , 1
        numerical_splits_count1 = deepcopy(numerical_splits_count)
        depth1 = deepcopy(depth)
        array.append(get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count1, depth1, iterations1, pct))
    return array

# get_graph will plot the points of the results from get_graph_data and return a graph
def get_graph(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, lower, upper, increment):
    '''
    get_graph - Given a training set, attribute metadata, validation set, numerical splits count, depth, iterations, lower(range),
    upper(range), and increment, this function will graph the results from get_graph_data in reference to the drange
    percentages of the data.
    '''
    get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations)
    pass