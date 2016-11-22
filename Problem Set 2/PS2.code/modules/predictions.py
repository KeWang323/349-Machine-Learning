import os.path
from operator import xor
from parse import *
#from node import 
from parse2 import parse2
from ID3 import handle_missing_value


# DOCUMENTATION
# ========================================
# this function outputs predictions for a given data set.
# NOTE this function is provided only for reference.
# You will not be graded on the details of this function, so you can change the interface if 
# you choose, or not complete this function at all if you want to use a different method for
# generating predictions.

def create_predictions(tree, predict):
    '''
    Given a tree and a url to a data_set. Create a csv with a prediction for each result
    using the classify method in node class.
    '''
    predict, attribute_metadata = parse2(predict, False)
    predict = handle_missing_value(predict,attribute_metadata)
    for i in range(0,len(predict)):
        predict[i][0] = tree.classify(predict[i])
        
        
    with open('./output/predict.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile,dialect='excel')
        for i in range(0,len(predict)):
            spamwriter.writerow(predict[i])
    