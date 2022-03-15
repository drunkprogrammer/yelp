import mxnet as mx
from mxnet import autograd, gluon, np, npx
from mxnet.gluon import nn
from d2l import mxnet as d2l
from split_data import split_and_load_yelp2013
from read_rating_matrix import read_sparse_rating_matrix
import csv

npx.set_np()

class MF(nn.Block):
    def __init__(self, num_factors, num_users, num_items, **kwargs):
        super(MF, self).__init__(**kwargs)
        self.P = nn.Embedding(input_dim=num_users, output_dim=num_factors)
        self.Q = nn.Embedding(input_dim=num_items, output_dim=num_factors)
        self.user_bias = nn.Embedding(num_users, 1)
        self.item_bias = nn.Embedding(num_items, 1)

    def forward(self, user_id, item_id):
        P_u = self.P(user_id)
        Q_i = self.Q(item_id)
        b_u = self.user_bias(user_id)
        b_i = self.item_bias(item_id)
        outputs = (P_u * Q_i).sum(axis=1) + np.squeeze(b_u) + np.squeeze(b_i) # axis = 1 base row

        return outputs.flatten()

def evaluator(net, test_iter, devices):
    rmse = mx.metric.RMSE()  # Get the RMSE
    rmse_list = []
    for idx, (users, items, ratings) in enumerate(test_iter):
        u = gluon.utils.split_and_load(users, devices, even_split=False)
        i = gluon.utils.split_and_load(items, devices, even_split=False)
        r_ui = gluon.utils.split_and_load(ratings, devices, even_split=False)
        r_hat = [net(u, i) for u, i in zip(u, i)]
        rmse.update(labels=r_ui, preds=r_hat)
        rmse_list.append(rmse.get()[1])
    return float(np.mean(np.array(rmse_list)))

def train_recsys_rating(net, train_iter, test_iter, loss, trainer, num_epochs,
                        devices=d2l.try_all_gpus(), evaluator=None,
                        **kwargs):
    timer = d2l.Timer()
    #animator = d2l.Animator(xlabel='epoch', xlim=[1, num_epochs], ylim=[0, 2], legend=['train loss', 'test RMSE'])
    for epoch in range(num_epochs):
        metric, l = d2l.Accumulator(3), 0.
        for i, values in enumerate(train_iter):
            timer.start()
            input_data = []
            values = values if isinstance(values, list) else [values]
            for v in values:
                input_data.append(gluon.utils.split_and_load(v, devices))
            train_feat = input_data[0:-1] if len(values) > 1 else input_data
            train_label = input_data[-1]
            with autograd.record():
                preds = [net(*t) for t in zip(*train_feat)]
                ls = [loss(p, s) for p, s in zip(preds, train_label)]
            [l.backward() for l in ls]
            l += sum([l.asnumpy() for l in ls]).mean() / len(devices)
            trainer.step(values[0].shape[0])
            metric.add(l, values[0].shape[0], values[0].size)
            timer.stop()
        if len(kwargs) > 0:  # It will be used in section AutoRec
            test_rmse = evaluator(net, test_iter, kwargs['inter_mat'],
                                  devices)
        else:
            test_rmse = evaluator(net, test_iter, devices)
        train_l = l / (i + 1)
        #animator.add(epoch + 1, (train_l, test_rmse))
    print(f'train loss {metric[0] / metric[1]:.3f}, '
          f'test RMSE {test_rmse:.3f}')
    print(f'{metric[2] * num_epochs / timer.sum():.1f} examples/sec '
          f'on {str(devices)}')

def predict_rating(net, sparse_matrix, filename):
    matrix_shape = sparse_matrix.shape
    devices = d2l.try_all_gpus()

    header3 = ["User ID", "Product ID", "Rating"]
    for i in range(matrix_shape[0]):
        for j in range(matrix_shape[1]):
            if sparse_matrix[i, j] == 0:
                p_score = net(np.array([i], dtype='int', ctx=devices[0]), np.array([j], dtype='int', ctx=devices[0]))
                sparse_matrix[i, j] = p_score

    with open(filename, 'w', encoding='UTF8', newline='') as f:
        for i in range(matrix_shape[0]):
            for j in range(matrix_shape[1]):
                f.write("  ".join(str(v) for v in [i, j, sparse_matrix[i, j]]))
                f.write("\n")

    f.close()
    return sparse_matrix


devices = d2l.try_all_gpus()
filename = './data/csv/yelp-2013-rating-matrix.csv'
num_users, num_items, train_iter, test_iter = split_and_load_yelp2013(
    feedback='explicit', test_ratio=0.1, batch_size=256, filename=filename)
net = MF(30, num_users, num_items)
net.initialize(ctx=devices, force_reinit=True, init=mx.init.Normal(0.01))
lr, num_epochs, wd, optimizer = 0.002, 20, 1e-5, 'adam'
loss = gluon.loss.L2Loss()
trainer = gluon.Trainer(net.collect_params(), optimizer,
                        {"learning_rate": lr, 'wd': wd})
train_recsys_rating(net, train_iter, test_iter, loss, trainer, num_epochs,
                    devices, evaluator)

rfilename1 = './data/csv/yelp-2013-rating-matrix.csv'
wfilename1 = './data/csv/yelp-2013-rating-prediction-matrix.txt'
sparse_matrix = read_sparse_rating_matrix(rfilename1)
predict_rating(net, sparse_matrix, wfilename1)


# predict_rating(net, sparse_matrix=upr_matrix, filename=wfilename3)


scores = predict_rating(net)
scores = net(np.array([20], dtype='int', ctx=devices[0]),
             np.array([30], dtype='int', ctx=devices[0]))
print(scores)