import math
from node import Node


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

def check_homogenous(data_set):
    '''
    ========================================================================================================
    Input:  A data_set
    ========================================================================================================
    Job:    Checks if the output value (index 0) is the same for all examples in the the data_set, if so return that output value, otherwise return None.
    ========================================================================================================
    Output: Return either the homogenous attribute or None
    ========================================================================================================
     '''
    for i in range(0, len(data_set)-1):
        if data_set[i][0] != data_set[i + 1][0]:
            return None
    return data_set[0][0]
    pass
# ======== Test Cases =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  None
# data_set = [[0],[1],[None],[0]]
# check_homogenous(data_set) ==  None
# data_set = [[1],[1],[1],[1],[1],[1]]
# check_homogenous(data_set) ==  1

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
                ratio,th = gain_ratio_numeric(data_set,attr,1)
                if ratiomax < ratio:
                    ratiomax = ratio
                    bestattribute = attr
                    splitvalue = th
    return bestattribute, splitvalue

# # ======== Test Cases =============================
# numerical_splits_count = [20,20]

# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "opprundifferential",'is_nominal': False}]
# data_set = [[1, 0.27], [0, 0.42], [0, 0.86], [0, 0.68], [0, 0.04], [1, 0.01], [1, 0.33], [1, 0.42], [0, 0.51], [1, 0.4]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, 0.51)

# attribute_metadata = [{'name': "winner",'is_nominal': True},{'name': "weather",'is_nominal': True}]
# data_set = [[0, 0], [1, 0], [0, 2], [0, 2], [0, 3], [1, 1], [0, 4], [0, 2], [1, 2], [1, 5]]
# pick_best_attribute(data_set, attribute_metadata, numerical_splits_count) == (1, False)

# Uses gain_ratio_nominal or gain_ratio_numeric to calculate gain ratio.

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
# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[1],[1]]
# mode(data_set) == 1
# data_set = [[0],[1],[0],[0]]
# mode(data_set) == 0

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

# ======== Test case =============================
# data_set = [[0],[1],[1],[1],[0],[1],[1],[1]]
# entropy(data_set) == 0.811
# data_set = [[0],[0],[1],[1],[0],[1],[1],[0]]
# entropy(data_set) == 1.0
# data_set = [[0],[0],[0],[0],[0],[0],[0],[0]]
# entropy(data_set) == 0


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
# ======== Test case =============================
# data_set, attr = [[1, 2], [1, 0], [1, 0], [0, 2], [0, 2], [0, 0], [1, 3], [0, 4], [0, 3], [1, 1]], 1
# gain_ratio_nominal(data_set,attr) == 0.11470666361703151
# data_set, attr = [[1, 2], [1, 2], [0, 4], [0, 0], [0, 1], [0, 3], [0, 0], [0, 0], [0, 4], [0, 2]], 1
# gain_ratio_nominal(data_set,attr) == 0.2056423328155741
# data_set, attr = [[0, 3], [0, 3], [0, 3], [0, 4], [0, 4], [0, 4], [0, 0], [0, 2], [1, 4], [0, 4]], 1
# gain_ratio_nominal(data_set,attr) == 0.06409559743967516

def gain_ratio_numeric(data_set, attribute, steps):
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
# ======== Test case =============================
# data_set,attr,step = [[1,0.05], [1,0.17], [1,0.64], [0,0.38], [1,0.19], [1,0.68], [1,0.69], [1,0.17], [1,0.4], [0,0.53]], 1, 2
# gain_ratio_numeric(data_set,attr,step) == (0.31918053332474033, 0.64)
# data_set,attr,step = [[1, 0.35], [1, 0.24], [0, 0.67], [0, 0.36], [1, 0.94], [1, 0.4], [1, 0.15], [0, 0.1], [1, 0.61], [1, 0.17]], 1, 4
# gain_ratio_numeric(data_set,attr,step) == (0.11689800358692547, 0.94)
# data_set,attr,step = [[1, 0.1], [0, 0.29], [1, 0.03], [0, 0.47], [1, 0.25], [1, 0.12], [1, 0.67], [1, 0.73], [1, 0.85], [1, 0.25]], 1, 1
# gain_ratio_numeric(data_set,attr,step) == (0.23645279766002802, 0.29)

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
# ======== Test case =============================
# data_set, attr = [[0, 4], [1, 3], [1, 2], [0, 0], [0, 0], [0, 4], [1, 4], [0, 2], [1, 2], [0, 1]], 1
# split_on_nominal(data_set, attr) == {0: [[0, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3]], 4: [[0, 4], [0, 4], [1, 4]]}
# data_set, attr = [[1, 2], [1, 0], [0, 0], [1, 3], [0, 2], [0, 3], [0, 4], [0, 4], [1, 2], [0, 1]], 1
# split on_nominal(data_set, attr) == {0: [[1, 0], [0, 0]], 1: [[0, 1]], 2: [[1, 2], [0, 2], [1, 2]], 3: [[1, 3], [0, 3]], 4: [[0, 4], [0, 4]]}

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
    pass
# ======== Test case =============================
# d_set,a,sval = [[1, 0.25], [1, 0.89], [0, 0.93], [0, 0.48], [1, 0.19], [1, 0.49], [0, 0.6], [0, 0.6], [1, 0.34], [1, 0.19]],1,0.48
# split_on_numerical(d_set,a,sval) == ([[1, 0.25], [1, 0.19], [1, 0.34], [1, 0.19]],[[1, 0.89], [0, 0.93], [0, 0.48], [1, 0.49], [0, 0.6], [0, 0.6]])
# d_set,a,sval = [[0, 0.91], [0, 0.84], [1, 0.82], [1, 0.07], [0, 0.82],[0, 0.59], [0, 0.87], [0, 0.17], [1, 0.05], [1, 0.76]],1,0.17
# split_on_numerical(d_set,a,sval) == ([[1, 0.07], [1, 0.05]],[[0, 0.91],[0, 0.84], [1, 0.82], [0, 0.82], [0, 0.59], [0, 0.87], [0, 0.17], [1, 0.76]])


def check_attribute_separable(data_set,attribute):# separable: 2     non-separable: 1
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