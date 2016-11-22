import json
import unittest
import numpy as np

import fnn
import mnist_experiment as me
import check_grad as cg


with open('toy_dataset.json', 'r') as f:
    toy_dataset = json.load(f)

toy_data = np.array(toy_dataset['data'][:10])
toy_labels = np.array(toy_dataset['labels'][:10])


class TestFNN(unittest.TestCase):
    def setUp(self):
        np.random.seed(seed=349)
        self.model = fnn.FNN(784, 10, [16, 8], [fnn.relu, fnn.relu])

    def test_forwardprop(self):
        # Used to check the whether bias is dealt correctly
        # in forwardprop.
        self.model.layers[-1].b[0][0] = 1.0
        probs, loss = self.model.forwardprop(toy_data, toy_labels)
        self.assertTrue(abs(loss - 2.3677889) < 0.0000001)
        print '\n' + '=' * 50 + '\n'
        print "Your forward propagation is correct!"
        print '\n' + '=' * 50 + '\n'

    def test_backprop(self):
        self.assertTrue(
            cg.check_backprop(self.model, toy_data, toy_labels) < 1e-4)
        print '\n' + '=' * 50 + '\n'        
        print "Your backpropagation is correct!"
        print '\n' + '=' * 50 + '\n'


if __name__ == '__main__':
    unittest.main()
