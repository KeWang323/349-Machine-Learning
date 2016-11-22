# DOCUMENTATION
# =====================================
# Class node attributes:
# ----------------------------
# children - dictionary containing the children where the key is child number (1,...,k) and the value is the actual node object
# if node has no children, self.children = None
# value - value at the node
#
#
# The values for bfs should be returned as simply a string of value space value space value. For example if the tree looks like the following:
#     5
#   2   3
#
# The tree data structure is a node with value 5, with a dictionary of children {1: b, 2: c} where b is a node with value 2 and c is a node with value 3.  Both b and c have children of None.
# The bfs traversal of the above tree should return the string '5 2 3'
from collections import deque
class Node:
	def __init__(self):
		self.value = None
		self.children = None

	def get_value(self):
		return(self.value)

	def get_children(self):
		return self.children

def breadth_first_search(root):
	if root is None:
		return []
	tree = deque([root])

	while tree:
		vertex = tree.popleft()
		print vertex.value,
		if vertex.get_children() is not None:
			for i in range(len(vertex.get_children())):
				tree.append(vertex.get_children()[i+1])
	return ''

def tester():
	a = Node()
	a.value = 5
	b = Node()
	b.value = 2
	c = Node()
	c.value = 3
	a.children = {1: b,2:c}
	print str(a.get_value()) + ' should be 5.'
	print str(a.get_children()) + ' should be {1: ' + str(b) + ', 2:' + str(c) + '}.'
	print str(breadth_first_search(a)) + ' should be 5 2 3.'

tester()