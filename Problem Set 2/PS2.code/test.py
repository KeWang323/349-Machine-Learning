import math
import numpy as np
from operator import xor
from random import shuffle
import random
import csv
from copy import deepcopy 
class Node:
    def __init__(self):
        # initialize all attributes
        self.label = None
        self.decision_attribute = None
        self.is_nominal = None
        self.value = None
        self.splitting_value = None
        self.children = {}
        self.name = None

    def classify(self, instance):
        if self.label != None:#no child
            return self.label
        else:# children exist
            if self.is_nominal == True:
                for key in self.children.keys():
                    if key == instance[self.decision_attribute]:
                        return self.children[instance[self.decision_attribute]].classify(instance)
                    else:
                        mode_node(self)
                        return self.label
            else:
                if instance[self.decision_attribute] < self.splitting_value:
                    return self.children[1].classify(instance)
                else:
                    return self.children[2].classify(instance)
    pass


    def print_help(self, n, indent = 0):
        tree = indent * "|  "
        if n.label is not None:
            return tree + "--->" + str(n.label) + "\n"
        elif n.is_nominal:
            space = ''
            for key, value in n.children.items():
                tree += space + str(n.name) + " = " + str(key) + "\n" + n.print_help(value, indent + 1)
                space = indent * "|  "
            return tree
        elif n.splitting_value is not None:
            symbol = ['', " < ", " >= "]
            space = ''
            for key, value in n.children.items():
                tree += space + str(n.name) + symbol[key] + str(n.splitting_value) + "\n" + n.print_help(value, indent+1)
                space = indent * "|  "
            return tree
        else:
            return ''
    
    def print_tree(self, indent = 0):
        '''
        returns a string of the entire tree in human readable form
        IMPLEMENTING THIS FUNCTION IS OPTIONAL
        '''
        return self.print_help(self, indent)
        
    def print_dnf_help(self, n, s = []):
        if n.label is not None:
            return ['('] + s + ['*'] + [n.label] + [')'] + ['|']
        elif n.is_nominal:
            string = []
            for key, value in n.children.items():
                string += n.print_dnf_help(value, s + [str(n.name) + " = " + str(key)])
            return string
        elif n.splitting_value is not None:
            string = []
            symbol = ['', " < ", " >= "]
            for key, value in n.children.items():
                string += n.print_dnf_help(value, s + [str(n.name) + symbol[key] + str(n.splitting_value)])
            return string
        else:
            return ['('] + s + [')'] + ['|']


    def print_dnf_tree(self):
        '''
        returns the disjunct normalized form of the tree.
        '''
        tree = self.print_dnf_help(self, [])
        print tree[0]
        dnf_tree = tree[0]
        f = True
        for each in range(1, len(tree) - 1):
            print "in the loop", tree[each]
            if tree[each] == '(' or tree[each] == ')':
                print "find ()"
                dnf_tree += str(tree[each])
                f = True
            elif tree[each] == '|':
                print "find |"
                dnf_tree += "OR\n"
                f = True
            elif tree[each] == '*':
                print "find *"
                dnf_tree += "--->"
                f = True
            else:
                if f:
                    dnf_tree += str(tree[each])
                else:
                    dnf_tree += "AND" + str(tree[each])
                    f = False
        dnf_tree += "\n"
        return dnf_tree
    
#def breadth_first_search(root, dictionary):
#    if root.label != None:
#        return dictionary
#    else:
#        children = get_children(root)
#        dictionary += children
#    return dictionary

def validation_accuracy(tree,validation_set):
    '''
    takes a tree and a validation set and returns the accuracy of the set on the given tree
    '''
    count = 0.0
    for entry in validation_set:
        if tree.classify(entry) == entry[0]:
            count += 1
    return count/len(validation_set) * 100
    pass
      
def entropy(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Calculates the entropy of the attribute at the 0th index, the value we want to predict.
    ========================================================================================================
    Output: Returns entropy. See Textbook for formula
    ========================================================================================================
    '''
    length = len(data_set)
    if length == 0:
        return NoData
    freqAttr = {}
    for entry in data_set:
        if freqAttr.has_key(entry[0]):
            freqAttr[entry[0]] += 1.0
        else:
            freqAttr[entry[0]] = 1.0
    Entropy = 0
    for value in freqAttr.values():
        Entropy = Entropy -value/length * math.log(value/length, 2)
    return Entropy

data_set11 = [[0],[1],[1],[1],[0],[1],[1],[1]]
data_set12 = [[0],[1],[1],[1],[0],[2],[3],[3]]
#print(entropy(data_set11))

def mode_node(node):
    if node.children is None:
        return
    else:
        count = []
        node_now = [node]
        while node_now:
            node_next = []
            for i in node_now:
                if i is None:
                    continue
                else:
                    if i.label is not None:
                        count.append(i)
                    else:
                        for each in range(len(i.children)):
                            node_next.append(i.children.get(each + 1))
            node_now = node_next
        count_label = []
        for n in count:
            count_label.append([n.label])
        if len(count_label) == 1:
            node.label = count_label[0][0]
        elif len(count_label) > 1:
            node.label = mode(count_label)

def check_homogenous(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the attribute at index 0 is the same for the data_set, if so return output otherwise None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
    '''
    for i in range(0, len(data_set)-1):
        if data_set[i][0] != data_set[i + 1][0]:
            return None
    return data_set[0][0]
    pass
data_set21 = [[0],[1],[1],[1],[0],[1],[1],[1]]
data_set22 = [[1],[1],[1],[1],[None],[1],[1],[1]]
data_set23 = [[1],[1],[1],[1],[0],[0],[1],[1]]
#print(check_homogenous(data_set3))

def split_on_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  subset of data set, the index for a nominal attribute.
    ========================================================================================================
    Job:    Creates a dictionary of all values of the attribute.
    ========================================================================================================
    Output: Dictionary of all values pointing to a list of all the data with that attribute
    ========================================================================================================
    '''
    splitnominal = {}
    subset = []
    for entry in data_set:
        if splitnominal.has_key(entry[attribute]):
            splitnominal[entry[attribute]].append(entry)
        else:
            subset.append(entry)
            splitnominal[entry[attribute]] = subset
            subset = []
    return splitnominal
data_set31, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
#print(split_on_nominal(data_set31, attr))

def mode(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Takes a data_set and finds mode of index 0.
    ========================================================================================================
    Output: mode of index 0.
    ========================================================================================================
    '''
    mode = {}
    for entry in data_set:
        if mode.has_key(entry[0]):
            mode[entry[0]] += 1.0
        else:
            mode[entry[0]] = 1.0
    maximum = max(mode.values())
    for key in mode.keys():
        if mode[key] == maximum:
            return key
    pass
data_set41 = [[0],[1],[1],[1],[1],[1]]
data_set42 = [[0]]
data_set43 = [[0],[0],[0],[1],[1],[1]]

#print(mode(data_set43))

def split_on_numerical(data_set, attribute, splitting_value):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, threshold (splitting) value
    ========================================================================================================
    Job:    Splits data_set into a tuple of two lists, the first list contains the examples where the given
	attribute has value less than the splitting value, the second list contains the other examples
    ========================================================================================================
    Output: Tuple of two lists as described above
    ========================================================================================================
    '''
    splitsmaller = []
    splitlarger = []
    for entry in data_set:
        if entry[attribute] >= splitting_value:
            splitlarger.append(entry)
        else:
            splitsmaller.append(entry)
    return (splitsmaller, splitlarger)
d_set51,a51,sval51 = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
d_set52,a52,sval52 = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
#print(split_on_numerical(d_set52,a52,sval52))

def gain_ratio_nominal(data_set, attribute):
    '''
    ========================================================================================================
    Input:  Subset of data_set, index for a nominal attribute
    ========================================================================================================
    Job:    Finds the gain ratio of a nominal attribute in relation to the variable we are training on.
    ========================================================================================================
    Output: Returns gain_ratio. See https://en.wikipedia.org/wiki/Information_gain_ratio
    ========================================================================================================
    '''
    length = len(data_set)
    info = entropy(data_set)
    dic = {}
    splitinfo = 0.0
    subsetinfo = 0.0
    for entry in data_set:
        if dic.has_key(entry[attribute]):
            dic[entry[attribute]] += 1.0
        else:
            dic[entry[attribute]] = 1.0
    for key in dic.keys():
        prob = dic[key]/length
        splitinfo += -prob * math.log(prob, 2)
        subset = []
        for entry in data_set:
            if entry[attribute] == key:
                subset.append(entry)
        subsetinfo += entropy(subset) * prob
    gain = info - subsetinfo
    gain_ratio = gain/splitinfo
    return gain_ratio
data_set61, attr61 = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
data_set62, attr62 = [[1,0.05], [1,0.17], [1,0.64], [0,0.38], [1,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1
data_set63, attr63 = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]],1
#print(gain_ratio_nominal(data_set63, attr63))

def gain_ratio_numeric(data_set, attribute,steps):
    '''
    ========================================================================================================
    Input:  Subset of data set, the index for a numeric attribute, and a step size for normalizing the data.
    ========================================================================================================
    Job:    Calculate the gain_ratio_numeric and find the best single threshold value
            The threshold will be used to split examples into two sets
                 those with attribute value GREATER THAN OR EQUAL TO threshold
                 those with attribute value LESS THAN threshold
            Use the equation here: https://en.wikipedia.org/wiki/Information_gain_ratio
            And restrict your search for possible thresholds to examples with array index mod(step) == 0
    ========================================================================================================
    Output: This function returns the gain ratio and threshold value
    ========================================================================================================
    '''
    length = len(data_set)
    info = entropy(data_set)
    ratiomax = 0.0
    th = 0
    for threshold in range(0, len(data_set)):
        if threshold % steps == 0:
            split0,split1 = split_on_numerical(data_set, attribute, data_set[threshold][attribute])
            if split0 != [] and split1 != []:
                prob0 = float(len(split0)) / length
                prob1 = float(len(split1)) / length
                gain = info - prob0 * entropy(split0) - prob1 * entropy(split1)
                Intrin = -prob0 * math.log(prob0, 2) - prob1 * math.log(prob1, 2)
                ratio = gain / Intrin
                if ratiomax < ratio:
                    ratiomax = ratio
                    th = data_set[threshold][attribute]
    return ratiomax, th
data_set71,attr71,step = [[0,0.05], [1,0.17], [1,0.64], [0,0.38], [0,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
data_set72,attr72,step = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]], 1,1
#print(gain_ratio_numeric(data_set72, attr72,step))

def pick_best_attribute(data_set, attribute_metadata, numerical_splits_count):
    '''
    ========================================================================================================
    Input:  A data_set, attribute_metadata, splits counts for numeric
    ========================================================================================================
    Job:    Find the attribute that maximizes the gain ratio. If attribute is numeric return best split value.
            If nominal, then split value is False.
            If gain ratio of all the attributes is 0, then return False, False
            Only consider numeric splits for which numerical_splits_count is greater than zero
    ========================================================================================================
    Output: best attribute, split value if numeric
    ========================================================================================================
    '''
    ratiomax = 0
    bestattribute = False
    splitvalue = False
    for attr in range(1, len(attribute_metadata)):
        if numerical_splits_count[attr] > 0 and check_attribute_separable(data_set,attr) == 2:
            if attribute_metadata[attr]['is_nominal'] == True:
                ratio = gain_ratio_nominal(data_set, attr)
                if ratiomax < ratio:
                    ratiomax = ratio
                    bestattribute = attr
                    splitvalue = False
            else:
                ratio,th = gain_ratio_numeric(data_set,attr,4)
                if ratiomax < ratio:
                    ratiomax = ratio
                    bestattribute = attr
                    splitvalue = th
    return bestattribute, splitvalue
numerical_splits_count = [0,0]
attribute_metadata81 = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
data_set81 = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
attribute_metadata82 = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
data_set82 = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
#print(pick_best_attribute(data_set81, attribute_metadata81, numerical_splits_count))

def check_attribute_separable(data_set,attribute):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the output value (index 0) is the same for all examples in the the data_set, if so return that output value, otherwise return None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
     '''
    if len(data_set) > 1:
        for i in range(0, len(data_set) - 1):
            if data_set[i][attribute] != data_set[i + 1][attribute]:
                return 2
    else:
        return 1
    pass
data_setcas,attributecas = [[0,0.42]],1
#print (check_attribute_separable(data_setcas,attributecas))

def ID3_split(node,data_set, attribute_metadata, numerical_splits_count, depth):
    if depth == 0:
        node.label = mode(data_set)
    else:
        if node.is_nominal == True:
            splitnominal = split_on_nominal(data_set,node.decision_attribute)
            depth -= 1
            numerical_splits_count[node.decision_attribute] -= 1
            for key in splitnominal.keys():
                node.children[key] = Node()
                node.children[key].decision_attribute, node.children[key].splitting_value = pick_best_attribute(splitnominal[key], attribute_metadata, numerical_splits_count)
                if node.children[key].decision_attribute != False:
                    node.children[key].name = attribute_metadata[node.children[key].decision_attribute]['name']
                    node.children[key].is_nominal = attribute_metadata[node.children[key].decision_attribute]['is_nominal']
                    node.children[key] = ID3_split(node.children[key], splitnominal[key], attribute_metadata, numerical_splits_count, depth)
                else:
                    node.children[key].label = mode(splitnominal[key])
        else:
            n1 = Node()
            n2 = Node()
            node.children = {1: n1, 2: n2}
            split1,split2 = split_on_numerical(data_set, node.decision_attribute, node.splitting_value)
            numerical_splits_count[node.decision_attribute] -=1
            depth -= 1
            if check_homogenous(split1) == None:
                n1.decision_attribute, n1.splitting_value = pick_best_attribute(split1, attribute_metadata, numerical_splits_count)
                if n1.decision_attribute != False:
                    n1.name = attribute_metadata[n1.decision_attribute]['name']
                    n1.is_nominal = attribute_metadata[n1.decision_attribute]['is_nominal']
                    n1 = ID3_split(n1,split1, attribute_metadata, numerical_splits_count, depth)
                else:
                    n1.label = mode(split1)
            else:
                n1.label = mode(split1)
            if check_homogenous(split2) == None:
                n2.decision_attribute, n2.splitting_value = pick_best_attribute(split2, attribute_metadata, numerical_splits_count)
                if n2.decision_attribute != False:
                    n2.name = attribute_metadata[n2.decision_attribute]['name']
                    n2.is_nominal = attribute_metadata[n2.decision_attribute]['is_nominal']
                    n2 = ID3_split(n2,split2, attribute_metadata, numerical_splits_count, depth)
                else:
                    n2.label = mode(split2)
            else:
                n2.label = mode(split2)
    return node
            
    
def ID3(data_set, attribute_metadata, numerical_splits_count, depth):
    '''
    See Textbook for algorithm.
    Make sure to handle unknown values, some suggested approaches were
    given in lecture.
    ========================================================================================================
    Input:  A data_set, attribute_metadata, maximum number of splits to consider for numerical attributes,
	maximum depth to search to (depth = 0 indicates that this node should output a label)
    ========================================================================================================
    Output: The node representing the decision tree learned over the given data set
    ========================================================================================================

    '''    
    n = Node()
    n.decision_attribute, n.splitting_value = pick_best_attribute(data_set, attribute_metadata, numerical_splits_count)
    n.name = attribute_metadata[n.decision_attribute]['name']
    n.is_nominal = attribute_metadata[n.decision_attribute]['is_nominal']
    if depth == 0:
        n.label = mode(data_set)
    else:
        n = ID3_split(n, data_set, attribute_metadata, numerical_splits_count, depth)
    return n
            
attribute_metadata91 = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
attribute_metadata92 = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': True}]
data_set91 = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [1, 0.42], [0, 0.51], [1, 0.4]]
data_set92 = [[1, 0], [0, 1], [0, -1], [0, -1], [0, 1], [1, 0], [1, 0], [1, 1], [1, 0], [0, 1], [1, -1]]
numerical_splits_count91 = [5, 5]
depth91 = 5
#n = ID3(data_set91, attribute_metadata91, numerical_splits_count91, depth91)
#print(n)
#n.print_tree('')

def handle_missing_value(data_set,attribute_metadata):
    for i in range(1, len(attribute_metadata)):
        if attribute_metadata[i]['is_nominal'] == True:
            subset = []
            for entry in data_set:
                if entry[i] != None:
                    subset.append([entry[i]])
            predict = mode(subset)
            for j in range(0,len(data_set)):
                if data_set[j][i] == None:
                    data_set[j][i] = predict
        else:
            value = 0
            length = 0
            for entry in data_set:
                if entry[i] != None:
                    value = value + entry[i]
                    length += 1 
            predict = value/length
            for j in range(0, len(data_set)):
                if data_set[j][i] == None:
                    data_set[j][i] = predict
    return data_set


import csv, collections

# Note: nominal data are integers while numeric data consists of floats

options = {
    'train' : 'data/btrain.csv',
    'validate': 'data/bvalidate.csv',
    'predict': 'data/btest.csv',
    'limit_splits_on_numerical': 10,
    'limit_depth': 5,
    'print_tree': True,
    'print_dnf' : False,
    'prune' : 'data/bvalidate.csv',
    'learning_curve' : {
        'upper_bound' : 0.05,
        'increment' : 0.001
    }
}

def parse(filename, keep_unlabeled):
    '''
    takes a filename and returns attribute information and all the data in array of arrays
    This function also rotates the data so that the 0 index is the winner attribute, and returns
    corresponding attribute metadata
    '''
    # initialize variables
    array = []
    csvfile = open(filename,'rb')
    fileToRead = csv.reader(csvfile, delimiter=' ',quotechar=',')

    # skip first line of data
    fileToRead.next()

    # set attributes
    attributes = [
    {
        'name': "winpercent",
        'is_nominal': False
    },
    {
        'name': "oppwinningpercent",
        'is_nominal': False
    },
    {
        'name': "weather",
        'is_nominal': True
    },
    {
        'name': "temperature",
        'is_nominal': False
    },
    {
        'name': "numinjured",
        'is_nominal': False
    },
    {
        'name': "oppnuminjured",
        'is_nominal': False
    },
    {
        'name': "startingpitcher",
        'is_nominal': True
    },
    {
        'name': "oppstartingpitcher",
        'is_nominal': True
    },
    {
        'name': "dayssincegame",
        'is_nominal': False
    },
    {
        'name': "oppdayssincegame",
        'is_nominal': False
    },
    {
        'name': "homeaway",
        'is_nominal': True
    },
    {
        'name': "rundifferential",
        'is_nominal': False
    },
    {
        'name': "opprundifferential",
        'is_nominal': False
    },
    {
        'name': "winner",
        'is_nominal': True
    }]

    # iterate through rows of actual data
    for row in fileToRead:
        # change each line of data into an array
        temp =row[0].split(',')
        if (not keep_unlabeled) and (temp[len(attributes) - 1] == "?"):
            continue
        for i in range(len(temp)):
            # data preprocessing
            if temp[i] == '?':
                temp[i] = None
            elif attributes[i]['is_nominal']:
                temp[i] = int(temp[i])
            else:
                temp[i] = float(temp[i])

        # rotate data so that the target attribute is at index 0
        d = collections.deque(temp)
        d.rotate(1)
        array.append(list(d))

    array.pop()

    # rotate attributes so that it corresponds to the data
    attributes = collections.deque(attributes)
    attributes.rotate(1)
    attributes = list(attributes)
    return array, attributes
    
def create_predictions(tree, predict):
    '''
    Given a tree and a url to a data_set. Create a csv with a prediction for each result
    using the classify method in node class.
    '''
    predict, attribute_metadata = parse2(predict, False)
    predict = handle_missing_value(predict,attribute_metadata)
    for i in range(0,len(predict)):
        predict[i][0] = tree.classify(predict[i])
    return predict
    
def parse2(filename, keep_unlabeled):
    '''
    takes a filename and returns attribute information and all the data in array of arrays
    This function also rotates the data so that the 0 index is the winner attribute, and returns
    corresponding attribute metadata
    '''
    # initialize variables
    array = []
    csvfile = open(filename,'rb')
    fileToRead = csv.reader(csvfile, delimiter=' ',quotechar=',')

    # skip first line of data
    fileToRead.next()

    # set attributes
    attributes = [
    {
        'name': "winpercent",
        'is_nominal': False
    },
    {
        'name': "oppwinningpercent",
        'is_nominal': False
    },
    {
        'name': "weather",
        'is_nominal': True
    },
    {
        'name': "temperature",
        'is_nominal': False
    },
    {
        'name': "numinjured",
        'is_nominal': False
    },
    {
        'name': "oppnuminjured",
        'is_nominal': False
    },
    {
        'name': "startingpitcher",
        'is_nominal': True
    },
    {
        'name': "oppstartingpitcher",
        'is_nominal': True
    },
    {
        'name': "dayssincegame",
        'is_nominal': False
    },
    {
        'name': "oppdayssincegame",
        'is_nominal': False
    },
    {
        'name': "homeaway",
        'is_nominal': True
    },
    {
        'name': "rundifferential",
        'is_nominal': False
    },
    {
        'name': "opprundifferential",
        'is_nominal': False
    },
    {
        'name': "winner",
        'is_nominal': True
    }]

    # iterate through rows of actual data
    for row in fileToRead:
        # change each line of data into an array
        temp =row[0].split(',')
#        if (not keep_unlabeled) and (temp[len(attributes) - 1] == "?"):
#            continue
        for i in range(len(temp)):
            # data preprocessing
            if temp[i] == '?':
                temp[i] = None
            elif attributes[i]['is_nominal']:
                temp[i] = int(temp[i])
            else:
                temp[i] = float(temp[i])

        # rotate data so that the target attribute is at index 0
        d = collections.deque(temp)
        d.rotate(1)
        array.append(list(d))

    array.pop()

    # rotate attributes so that it corresponds to the data
    attributes = collections.deque(attributes)
    attributes.rotate(1)
    attributes = list(attributes)
    return array, attributes

def get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations, pct2):
    '''
    get_graph_accuracy_partial - Given a training set, attribute metadata, validation set, numerical splits count, and percentage,
    this function will return the validation accuracy of a specified (percentage) portion of the trainging setself.
    '''
    aver = 0
    for i in range(0,iterations):
        shuffle(train_set)
        temppart = []
        for j in range(0, int(len(train_set) * pct2)):
            temppart.append(train_set[j])
        numerical_splits_count1 = deepcopy(numerical_splits_count)
        depth1 = deepcopy(depth)
        tree = ID3(temppart, attribute_metadata, numerical_splits_count1, depth1)
        accuracy = validation_accuracy(tree,validate_set)
        aver = aver + accuracy
    aver = aver / iterations
    return aver
    
            
def get_graph_data(train_set, attribute_metadata, validate_set, numerical_splits_count, depth, iterations1):
    '''
    Given a training set, attribute metadata, validation set, numerical splits count, iterations, and percentages,
    this function will return an array of the averaged graph accuracy partials based off the number of iterations.
    '''
    array = []
    for pct in range(1, 11):
        pct = float(pct) / 10
        numerical_splits_count1 = deepcopy(numerical_splits_count)
        depth1 = deepcopy(depth)
        array.append(get_graph_accuracy_partial(train_set, attribute_metadata, validate_set, numerical_splits_count1, depth1, iterations1, pct))
    return array


train_set10, attribute_metadata10 = parse('D:/2016 Spring/349 Machine Learning/Problem Set 2/PS2.code/data/test_btrain.csv', False)
data_set_new10 = handle_missing_value(train_set10,attribute_metadata10)
numerical_splits_count10 = [5] * len(attribute_metadata10)
depth10 = 20
#n = ID3(data_set_new10, attribute_metadata10, numerical_splits_count10, depth10)
#print(n.print_tree())
#print(n.print_dnf_tree())
#

validate_set, _ = parse('D:/2016 Spring/349 Machine Learning/Problem Set 2/PS2.code/data/test_bvalidate.csv', False)
validate_set_new = handle_missing_value(validate_set,attribute_metadata10)
#print(depth10, validation_accuracy(n,validate_set_new))


#predict = create_predictions(n, 'D:/2016 Spring/349 Machine Learning/Problem Set 2/PS2.code/data/test_btest.csv')
#with open('./output/predict.csv', 'wb') as csvfile:
#    spamwriter = csv.writer(csvfile,dialect='excel')
#    for i in range(0,len(predict)):
#        spamwriter.writerow(predict[i])

iterations = 8
print(get_graph_data(data_set_new10, attribute_metadata10, validate_set_new, numerical_splits_count10, depth10, iterations))
#print(get_graph_accuracy_partial(data_set_new10, attribute_metadata10, validate_set_new, numerical_splits_count10, depth10, iterations, 0.5))