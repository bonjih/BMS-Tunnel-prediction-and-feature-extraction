from prepare.xysplit import get_log_time_in_cat
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity


def bucket_image():
    cat = "Network Performance"
    df = get_log_time_in_cat(cat)
    print(df)
    kd = KernelDensity(kernel="gaussian", bandwidth=0.2).fit(df["IncidentDetectionTime"])
    print(kd.score_samples(df["IncidentDetectionTime"]))
    plt.hist(df["IncidentDetectionTime"].values.astype(np.datetime64), bins=24, color='y')
    plt.xticks(rotation=45)
    plt.title(cat + " Hourly Distribution")
    plt.savefig("../../images/" + cat + "_daily_dist.png")
    plt.show()

bucket_image()
