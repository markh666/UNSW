import numpy as np

def logistic_regression(data, labels, weights, num_epochs, learning_rate): # do not change the heading of the function
    data = np.column_stack((np.ones(data.shape[0]), data))
    y = np.transpose(np.mat(labels))
    count = 0
    while count < num_epochs:
        theta = np.multiply(np.mat(data),np.mat(weights)).sum(axis = 1)
        h = np.array(1/(1+np.exp(-1.0*theta)))
        grad = np.hstack((y, -1*h)).sum(axis=1)
        weights = weights + learning_rate * (np.multiply(grad, data).sum(axis=0))
        count += 1
    weights = weights.tolist()[0]
    return weights
