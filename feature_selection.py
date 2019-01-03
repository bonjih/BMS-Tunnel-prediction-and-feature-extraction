import numpy as np
from matplotlib import pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.metrics import auc
from sklearn.metrics import confusion_matrix
from sklearn.metrics import mean_squared_error
from sklearn.metrics import roc_curve
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import normalize
from sklearn.utils.extmath import pinvh
from sklearn.svm import SVC, LinearSVC, NuSVC


from prepare.xysplit import get_normal_encoded_x_bin_enc_y, get_normal_encoded_x_and_y


def mutual_incoherence(X_relevant, X_irelevant):
    """Mutual incoherence, as defined by formula (26a) of [Wainwright2006].
    """
    projector = np.dot(np.dot(X_irelevant.T, X_relevant),
                       pinvh(np.dot(X_relevant.T, X_relevant)))
    return np.max(np.abs(projector).sum(axis=1))


def plot_confusion_matrix(cm, ax,classnames,title='Confusion matrix', cmap=plt.cm.Blues, ):
    ax.imshow(cm, interpolation='nearest', cmap=cmap)

    xy_font = {'family':'normal', 'weight' : 'bold', 'size': 14}
    label_font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 12}

    ax.set_title(title)
    ax.set_xlabel("Predicted Label", xy_font)
    ax.set_ylabel("True Label", xy_font)
    tick_marks = np.arange(len(classnames))
    ax.set_xticks(tick_marks)
    ax.set_yticks(tick_marks)



    ax.set_xticklabels(classnames, fontdict=label_font)
    ax.set_yticklabels(classnames, fontdict=label_font)
    # plt.tight_layout()
    # plt.ylabel('True label')
    # plt.xlabel('Predicted label')


def confusion_matrix_normal_x_binarized_y():
    X, y, x_encoders, y_encoder = get_normal_encoded_x_bin_enc_y(10000)
    X_norm = normalize(X.values)
    y_norm = normalize(y.values)
    X_train, X_test, y_train, y_test = train_test_split(X_norm, y_norm, train_size=0.3)
    print("Prediction Accuracy for all of: ", y.columns)

    f, axarr = plt.subplots(4,4)
    row = 0
    colu = 0
    for col in y.columns:
        # predictions
        idx = np.where(y.columns == col)[0][0]
        print("Predict: " , col)
        clf = AdaBoostClassifier(n_estimators=1000, learning_rate=0.3).fit(X_train, y_train[:,idx])
        score = clf.score(X_test, y_test[:,idx])
        print("\t Score: ", score)
        # con matrix
        cm = confusion_matrix(y_true=y_test[:,idx],y_pred=clf.predict(X_test))
        #plotting

        cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        plot_confusion_matrix(cm_normalized, axarr[row, colu], title=col)

        if (colu == 3):
            row += 1
            colu = 0
        else:
            colu += 1

    plt.show()

def confusion_matrix_normal_x_normal_y():
    X, y, x_encoders, y_encoder = get_normal_encoded_x_and_y(10000)
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.3)

    clf = RandomForestClassifier(n_jobs=-1, n_estimators=100, oob_score=True)
    clf.fit(X_train, y_train)

    score = clf.score(X_test, y_test)


    print("Feature Importances: " + str(clf.feature_importances_))
    print("\t Score: ", score)
    # con matrix
    y_pred = clf.predict(X_test)
    cm = confusion_matrix(y_true=y_test,y_pred=y_pred)
    mse = mean_squared_error(y_true=y_test, y_pred=y_pred)
    print("\t MSE: " ,mse)
    #plotting

    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    f, ax = plt.subplots(1, 1)
    plot_confusion_matrix(cm_normalized, ax, y_encoder.classes_,title="Confusion Matrix")
    plt.tight_layout()
    plt.annotate("MSE: " + str(mse), xy=(2,0))
    plt.annotate("Score: " + str(score), xy=(2,0.2))
    plt.show()


def ensemble_forest_plot_decision_tree():
    plot_step = 0.02
    plot_step_coarser = 0.5
    plot_colors = "ryb"
    cmap = plt.cm.RdYlBu

    X, y, x_encoders, y_encoder = get_normal_encoded_x_and_y(10000)
    n_classes = len(y_encoder.classes_)

    mean = X.mean(axis=0)
    std = X.std(axis=0)
    X = (X - mean) / std

    X_pair = (X[["detection", "Source"]]).values


    X_train, X_test, y_train, y_test = train_test_split(X_pair, y, train_size=0.3)

    clf = RandomForestClassifier(n_jobs=-1, n_estimators=100, oob_score=True)
    clf.fit(X_train, y_train)


    scores = clf.score(X_test, y_test)

    x_min, x_max = X_test[:, 0].min() - 1, X_test[:, 0].max() + 1
    y_min, y_max = X_test[:, 1].min() - 1, X_test[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step),
                         np.arange(y_min, y_max, plot_step))

    estimator_alpha = 1.0 / len(clf.estimators_)
    for tree in clf.estimators_:
        Z = tree.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        cs = plt.contourf(xx, yy, Z, alpha=estimator_alpha, cmap=cmap)

    # xx_coarser, yy_coarser = np.meshgrid(np.arange(x_min, x_max, plot_step_coarser),
    #                                     np.arange(y_min, y_max, plot_step_coarser))
    # Z_points_coarser = clf.predict(np.c_[xx_coarser.ravel(), yy_coarser.ravel()]).reshape(xx_coarser.shape)
    # cs_points = plt.scatter(xx_coarser, yy_coarser, s=15, c=Z_points_coarser, cmap=cmap, edgecolors="none")

    # Plot the training points, these are clustered together and have a
    # black outline
    for i, c in zip(range(0,n_classes), plot_colors):
        idx = np.where(y_test == i)
        plt.scatter(X_test[idx, 0], X_test[idx, 1], c=c,cmap=cmap)


    plt.show()

if __name__ == "__main__":
    ensemble_forest_plot_decision_tree()

