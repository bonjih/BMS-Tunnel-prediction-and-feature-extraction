from itertools import cycle

from prepare.xysplit import get_log_text_xy_split
from sklearn.cross_validation import train_test_split
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import numpy as np

X_obj, y_obj = get_log_text_xy_split(200)

X = np.array(X_obj).astype(str)
y = np.array(y_obj).astype(str)

X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=0.3)

vectorizor = TfidfVectorizer(max_df=2)
X_train = vectorizor.fit_transform(X_train_raw)
X_test = vectorizor.fit_transform(X_test_raw)

X_train_pca = TruncatedSVD(n_components=2).fit_transform(X_train)
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
markers = [".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "*", "h", "H", "+", "x", "D",
           "d", "|", "_"]
for i, c, m in zip(np.unique(y_train), cycle(colors), cycle(markers)):
    plt.scatter(X_train_pca[y_train == i, 0],
                X_train_pca[y_train == i, 1],
                c=c, label=i, alpha=0.5, marker=m, s=40)

plt.legend(loc='best')
plt.show()
