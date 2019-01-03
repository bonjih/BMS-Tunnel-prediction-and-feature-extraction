#Apply linear_svc to the dataset
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from prepare.xysplit import get_binary_encoded_xy_split
import matplotlib.pyplot as plt
clf = LinearSVC(fit_intercept=True, multi_class="ovr")
clf2 = KNeighborsClassifier()

# get basic x, y split

# Preliminary Investigations
# ===========================
# Best linear svc score at predicting `category` based on textual categorized data from columns
# selected in xysplit for linearsvc is 0.836 best kneighbours score with the same data is 0.81
# Largest dataset size in rows that i have used: 5000
# Largest dataset size possible is probably around 16000
#
X_train, X_test, y_train, y_test = get_binary_encoded_xy_split(5000)
clf.fit(X_train, y_train)
# clf2.fit(X_train, y_train)

print("Linear SVC score: ", clf.score(X_test, y_test))
# print("KNeighbors Score: ", clf2.score(X_test, y_test))
plt.scatter(x=range(0,y_test.shape[0]),y=y_test,marker="o",c="r")
plt.scatter(x=range(0,y_test.shape[0]),y=clf.predict(X_test), c="b")
plt.show()
