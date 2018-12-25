from netomaton import *
import mnist
from sklearn.linear_model import LogisticRegression
import time

if __name__ == '__main__':

    train_images = mnist.train_images()
    train_labels = mnist.train_labels()
    test_images = mnist.test_images()
    test_labels = mnist.test_labels()

    def binarize(image):
        image = image.reshape(28 * 28)
        return [1 if c > 0 else 0 for c in image]

    # [print("%s: %s" % (i, x)) for i,x in enumerate(train_labels)]

    r = 1
    k = 2
    rule_number = 512
    timesteps = 30
    n_train = len(train_images)
    n_test = len(test_images)
    print("r: %s; k: %s; rule: %s; timesteps: %s; # train: %s; # test: %s" % (r, k, rule_number, timesteps, n_train, n_test))

    adjacencies = AdjacencyMatrix.cellular_automaton2d(rows=28, cols=28, r=r, neighbourhood='Moore')

    X = []
    Y = []

    for i in range(n_train):
        initial_conditions = binarize(train_images[i])
        r = ReversibleRule(initial_conditions, lambda n, c, t: ActivityRule.totalistic_ca(n, k=k, rule=rule_number))
        activities, _ = evolve(initial_conditions, adjacencies, timesteps=timesteps, activity_rule=r.activity_rule)
        X.append(np.array(activities[-5:]).reshape(28*28*5).tolist())
        Y.append(train_labels[i])
        print("%s: class: %s" % (i, train_labels[i]))

    reg = LogisticRegression(multi_class='ovr')
    reg.fit(X, Y)

    # print(reg.coef_.shape) # there will be 10 * 28*28*30 coefficients

    num_correct = 0
    for j in range(n_test):
        initial_conditions = binarize(test_images[j])
        r = ReversibleRule(initial_conditions, lambda n, c, t: ActivityRule.totalistic_ca(n, k=k, rule=rule_number))
        activities, _ = evolve(initial_conditions, adjacencies, timesteps=timesteps, activity_rule=r.activity_rule)
        prediction = reg.predict([np.array(activities[-5:]).reshape(28*28*5).tolist()])
        print("prediction: %s; actual: %s" % (prediction, test_labels[j]))
        if prediction[0] == test_labels[j]:
            num_correct += 1

    print("%s / %s" % (num_correct, n_test))

    # animate(activities0, shape=(28, 28))

