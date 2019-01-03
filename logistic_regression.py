#Apply linear_svc to the dataset
from sklearn.linear_model import LogisticRegression
from prepare.xysplit import get_binary_encoded_xy_split
import matplotlib.pyplot as plt
from pandas import DataFrame
clf = LogisticRegression(fit_intercept=True, multi_class="ovr")

X_train, X_test, y_train, y_test, y_encoder = get_binary_encoded_xy_split(5000)
clf.fit(X_train, y_train)

print("Logistic Score: ", clf.score(X_test, y_test))
probs = DataFrame(clf.predict_proba(X_test))
print(probs.shape)
probs_norm = (probs - probs.mean()) / (probs.max() - probs.min())
probs_norm.columns = y_encoder.classes_
probs_norm.hist()
plt.show()


