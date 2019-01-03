from prepare.xysplit import get_binary_encoded_xy_split
from sklearn.decomposition import RandomizedPCA
from sklearn.decomposition import FastICA
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble.partial_dependence import plot_partial_dependence
from matplotlib import pyplot as plt
import numpy as np


# No real meaningful information was found here
def main():
    X_train, X_test, y_train, y_test, y_encoder = get_binary_encoded_xy_split(5000)
    # reduce 1000 X 1024 dimensions to 11 (number of X columns before label binarization in table)
    X_train_randPCA = RandomizedPCA()
    X_train_randPCA.fit(X_train)
    print("pca fit")

    X_train_reduced = X_train_randPCA.transform(X_train)
    X_test_reduced = X_train_randPCA.transform(X_test)

    print("Reduced components")
    print("Begin classifier")
    clf = GradientBoostingClassifier(n_estimators=200, max_depth=4, learning_rate=0.1, random_state=1)
    print(y_train.shape, y_test.shape)
    print(y_encoder.classes_)
    print(y_encoder.transform(["Accident"]))
    print(np.where(y_encoder.classes_ == "Accident"))
    clf.fit(X_train_reduced, y_train[:, np.where(y_encoder.classes_=="Accident")[0]])
    print("Fitted")
    print("_" * 80)
    feature_vals = y_encoder.transform(y_encoder.classes_)
    feature_labels = y_encoder.classes_
    print(feature_vals)
    print(feature_labels)
    fig, axs = plot_partial_dependence(clf, X_train,[0,1], n_jobs=4, grid_resolution=100)
    plt.show()


if __name__ == "__main__":
    main()
