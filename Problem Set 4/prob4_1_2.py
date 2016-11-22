import csv, random
def J48_KNN():
    '''
    This function writes a data set to perform very well on J48, and not as well using k nearest neighbor classifier.
    '''
    f = csv.writer(open('prob4_1.txt', 'wb'))
    head = []
    for i in range(50):
        head.append('X' + str(i+1))
    head.append('Y')
    f.writerow(head)
    for i in range(1000):
        row = []
        for j in range(50):
            pred_val = random.randint(0,1)
            row.append(pred_val)
        if (row[25] == 1 and row[1] == 0) or (row[13] == 0 and row[26] == 1) or (row[12] == 0 and row[23] == 0)or (row[16] == 0 and row[28] == 0):
            row.append(1)
        else:
            row.append(0)
        f.writerow(row)


def NB_MLP():
    '''
    This function writes a data set to perform very well on multi-layer perceptrons, and not as well using naive bayes classifier.
    '''
    f = csv.writer(open('prob4_2.txt', 'wb'))
    head = []
    for i in range(2):
        head.append('X' + str(i+1))
    head.append('Y')
    f.writerow(head)
    for i in range(1000):
        row = []
        for j in range(2):
            row.append(random.randint(0,1))
        if row[0] == row[1]:
                row.append(0)
        else:
            row.append(1)
        f.writerow(row)

J48_KNN()
NB_MLP()