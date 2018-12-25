import mnist
from sklearn.linear_model import LogisticRegression

if __name__ == '__main__':

    train_images = mnist.train_images()
    train_labels = mnist.train_labels()

    def binarize(image):
        image = image.reshape(28 * 28)
        return [1 if c > 0 else 0 for c in image]

    X = []
    Y = []
    n_train = 1000 #len(train_images)

    for i in range(n_train):
        X.append(binarize(train_images[i]))
        Y.append(train_labels[i])
        print("%s: class: %s" % (i, train_labels[i]))

    reg = LogisticRegression(multi_class='ovr')
    reg.fit(X, Y)

    test_images = mnist.test_images()
    test_labels = mnist.test_labels()
    num_correct = 0
    n_test = 100 #len(test_images)
    for j in range(n_test):
        prediction = reg.predict([binarize(test_images[j])])
        print("prediction: %s; actual: %s" % (prediction, test_labels[j]))
        if prediction[0] == test_labels[j]:
            num_correct += 1

    print("%s / %s" % (num_correct, n_test))
