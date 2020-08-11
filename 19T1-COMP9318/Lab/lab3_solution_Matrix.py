# https://blog.csdn.net/ustbbsy/article/details/80423294
# https://blog.csdn.net/u010837794/article/details/70991434
# https://blog.csdn.net/baimafujinji/article/details/51175830
import numpy as np
def logistic_regression(data, labels, weights, num_epochs, learning_rate):
    n = data.shape[0] # data shape 一共多少行
    data = np.insert(data, 0, np.ones(n), axis = -1) # 往最前面插了一列, 每个都是 1
    data = np.mat(data)
    labels = np.mat(labels).T # label转置成竖列
    weights = np.mat(weights)
    for i in range(0, num_epochs):
        dot = np.multiply(data, weights).sum(axis = 1)
        # wtight is a b c , data是每行的 x y 1, 所以 dot 计算的是 ax+ by + c 的值,dot是n行 一列
        h = 1 / (1 + np.exp(-1.0 * dot))
        # 这个h图像画出来, 可以实现一个分类器的功能,分类到0或1 . 并且h是可以求导的,
        # 比如带图 dot=5 时, 就很接近1.
        # h 计算出来是n行 一列
        h = np.array(h) #格式转化, 防止报错
        # if h and labels 不相同. lebel=1 h=0 or lebel =0 h =1 求出grad 放入line20
        # if h and label 相同 pass
        grad = np.hstack((labels, -1 * h)).sum(axis = 1)
        weights = weights + learning_rate * (np.multiply(grad, data).sum(axis = 0))
    weights = weights.tolist()[0]
    return weights
