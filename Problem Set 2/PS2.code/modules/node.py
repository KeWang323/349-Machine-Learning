# DOCUMENTATION
# =====================================
# Class node attributes:
# ----------------------------
# children - a list of 2 nodes if numeric, and a dictionary (key=attribute value, value=node) if nominal.  
#            For numeric, the 0 index holds examples < the splitting_value, the 
#            index holds examples >= the splitting value
#
# label - is None if there is a decision attribute, and is the output label (0 or 1 for
#	the homework data set) if there are no other attributes to split on or the data is homogenous
#       
#
# decision_attribute - the index of the decision attribute being split on
#
# is_nominal - is the decision attribute nominal
#
# value - Ignore (not used, output class if any goes in label)
#
# splitting_value - if numeric, where to split
#
# name - name of the attribute being split on

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
        if self.label != None:#no child then returen the label
            return self.label
        else:# children exist
            if self.is_nominal == True:
                for key in self.children.keys():
                    if key == instance[self.decision_attribute]:#find the k
                        return self.children[instance[self.decision_attribute]].classify(instance)
                    else:
                        return False
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