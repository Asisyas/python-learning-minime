import tflearn

class Model_Factory:
    def create_model(self, train_x, train_y):
        net = tflearn.input_data(shape=[None, len(train_x[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
        net = tflearn.regression(net)

        model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

        return model
