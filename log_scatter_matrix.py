from prepare.xysplit import get_binary_encoded_xy_split
from pandas.tools.plotting import scatter_matrix
from pandas import DataFrame
from sklearn.naive_bayes import BernoulliNB
from sklearn.decomposition import RandomizedPCA
# Export images on linux
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

def log_scatter_matrix_report():
    X_train, X_test, y_train, y_test, y_encoder = get_binary_encoded_xy_split(1000)
    df = DataFrame(X_train)
    # scatter_matrix(df, alpha=0.2, figsize=(25, 25), diagonal='kde')
    clf = BernoulliNB()
    clf.fit(X_train, y_train)
    probas = DataFrame(clf.predict_proba(X_train), columns=y_encoder.classes_)
    probas.hist()
    plt.subplots_adjust(top=1)

    plt.savefig("../../images/bernouli_classifier_score_distribution.png")

log_scatter_matrix_report()
