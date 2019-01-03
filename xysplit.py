from sklearn.preprocessing import LabelEncoder
from sqlalchemy import Table

from dbconnect.auto_bms_wrapper import AutoBMSWrapper
from dbconnect.alchemy_models import Log, Breakdown
from pandas import DataFrame
from pandas import Series
from sqlalchemy import text
import numpy as np
import pandas as pd
from functools import reduce
from sklearn.cross_validation import train_test_split
from sqlalchemy.sql.expression import func, select
from sqlalchemy.sql.expression import _literal_as_text
from sklearn.preprocessing import LabelBinarizer

def get_log_text_xy_split(sample_size):
    """
    Return X, y: where y is the tablename of the element of X
    """
    # initialize database connection
    db_wrapper = AutoBMSWrapper()
    session = db_wrapper.session
    # Get list of log id's

    log_ids = Series(session.query(Log.logid).all()).sample(sample_size).values
    log_ids = [x for y in log_ids for x in y]
    # Get sample of log ids
    # log_ids = np.array(log_ids.toList())
    Xy = DataFrame(session.query(Log.logid, Log.Category, Log.Description).filter(Log.logid.in_(log_ids)).all());
    X = Xy["Description"]
    y = Xy["Category"]

    session.close()
    return X, y


def get_log_time_in_cat(category:str ="breakdown"):
    session = AutoBMSWrapper().session
    df = DataFrame.from_dict(session.query(func.TIME(Log.IncidentDetection).label("IncidentDetectionTime"), Log.Category).filter(Log.Category==category).all())
    return df


def get_log_xy(sample_size:int = 16000):
    """get a raw log dataframe of sample_size samples"""
    session = AutoBMSWrapper().session
    df = DataFrame.from_dict(session.query(Log.IncidentDate, Log.ControllerName, Log.IncidentType, Log.Direction,
                                           Log.Location, Log.SubLocation, Log.Lane, Log.Source, Log.Description,
                                           Log.IncidentDetection, Log.IncidentResponse, Log.ResponseDespatch,
                                           Log.SDTime, Log.ResponseOnsite, Log.IncidentClear, Log.Category,
                                           Log.Criticality, Log.Reporter, Log.Responder, Log.Closure, Log.Power,
                                           Log.Parent).order_by(func.RAND()).limit(sample_size).all())
    df=df.fillna(method="bfill").fillna(method="ffill")
    session.close()
    return df

def _get_log_useful_cols(sample_size):
    """
    Columns in returned DataFrame:: "ControllerName", "Direction", "Location", "SubLocation", "Lane", "Source", "Description", "Reporter", "Responder", "Category", "detection", "duration"
    """
    db_wrapper = AutoBMSWrapper()
    session = db_wrapper.session

    query = session.query(
        Log.ControllerName, Log.Direction, Log.Location, Log.SubLocation,
        Log.Lane, Log.Source, Log.Description, Log.Reporter, Log.Responder,
        Log.Category, func.TIME(Log.IncidentDetection).label('detection'),
        func.TIMESTAMPDIFF(_literal_as_text("SECOND"),Log.IncidentDetection, Log.IncidentClear).label("duration"))\
            .filter(Log.Category.notin_(["Fire Incident", "Accident", "Debris"]))\
            .order_by(func.RAND())\
            .limit(sample_size).all()

    # We are done with the database connection now, lets not leave 10^6 threads open on the server #
    session.close()

    df = DataFrame.from_dict(query)
    df.columns = ["ControllerName", "Direction", "Location", "SubLocation", "Lane", "Source", "Description", "Reporter",
                  "Responder", "Category", "detection", "duration"]
    return df


def get_binary_encoded_xy_split(sample_size):
    """
    Return feature set encoded as binary sparse matrix
    i.e
    ╔═════╦═══════════════╦═════════════════╦═════════════════════╦═════╗
    ║ Row ║ IncidentType  ║                 ║                     ║ ... ║
    ╠═════╬═══════════════╬═════════════════╬═════════════════════╬═════╣
    ║     ║ Fire Incident ║ Failure(System) ║ Failure (Structure) ║ ... ║
    ║   0 ║ 1             ║ 0               ║ 0                   ║ ... ║
    ║   1 ║ 0             ║ 1               ║ 0                   ║ ... ║
    ╚═════╩═══════════════╩═════════════════╩═════════════════════╩═════╝

    :param sample_size number of rows to return (pseudorandomly selected with MySQL RAND function)
    :return: query result
    """
    Xy = _get_log_useful_cols(sample_size)

    categorical = ["ControllerName", "Direction", "Location", "SubLocation", "Lane", "Source", "Description", "Reporter", "Responder"]
    # categorical = ["Direction"]
    X = Xy[categorical]
    X=X.fillna(method="ffill").fillna(method="bfill")
    label = Xy["Category"].fillna(method="ffill").fillna("bfill")

    y_encoder = LabelEncoder().fit(label)
    print("Encoder Params: ", y_encoder.get_params())
    y_enc = y_encoder.transform(label)
    X_enc_ls = [LabelBinarizer().fit_transform(X[cn]) for cn in X.columns]
    Xy["detection"] = Xy["detection"].apply(lambda x: x / np.timedelta64(1,'s'))

    fn = lambda x, y: np.hstack((x,y))
    X_enc = reduce(fn, X_enc_ls)
    X_enc = np.hstack((X_enc, Xy[["detection", "duration"]].values))
    print(X_enc.shape)
    X_train, X_test, y_train, y_test = train_test_split(X_enc, y_enc, test_size=0.3)
    return X_train, X_test, y_train, y_test, y_encoder


def get_normal_encoded_x_bin_enc_y(sample_size):
    """
    Return feature set encoded as numbers and label in binarized form
    ╔═════╦══════════════╗
    ║ Row ║ IncidentType ║
    ╠═════╬══════════════╣
    ║   0 ║            3 ║
    ║   1 ║            6 ║
    ║   3 ║            7 ║
    ║   5 ║            4 ║
    ╚═════╩══════════════╝
    :param sample_size:
    :return: X_train, X_test, y_train, y_test, X_encoders[], y_encoder
    """
    Xy = _get_log_useful_cols(sample_size)

    feature_set_cols = ["Direction", "Location", "SubLocation", "Lane", "Source", "duration"]
    label_set_cols = ["Category"]
    categorical = feature_set_cols[0:5]

    # Textual --> Numerical Categories
    label_encoders = {}
    for column_name in categorical:
        le = LabelEncoder().fit(Xy[column_name])
        Xy[column_name] = le.transform(Xy[column_name])
        label_encoders[column_name] = le

    print(Xy["Direction"])
    X = Xy[feature_set_cols]
    y = Xy["Category"].fillna("Information")

    y_binarizer = LabelBinarizer().fit(y)
    print(y_binarizer.classes_)
    y_encoded = DataFrame(y_binarizer.transform(y))
    y_encoded.columns = y_binarizer.classes_

    # Validate my thinking about how encoder works

    # print(y_binarizer.inverse_transform(y_encoded))
    # print("-" * 80)
    # print(y_encoded)
    # print("-" * 80)
    # print(y_binarizer.inverse_transform(y_encoded.values))


    # Xy.columns = ["ControllerName", "Direction", "Location", "SubLocation", "Lane", "Source", "Description", "Reporter",
    #              "Responder", "Category", "detection", "duration"]
    return X, y_encoded, label_encoders, y_binarizer


def get_normal_encoded_x_and_y(sample_size):
    """
    Return feature set encoded as numbers and label in binarized form
    ╔═════╦══════════════╗
    ║ Row ║ IncidentType ║
    ╠═════╬══════════════╣
    ║   0 ║            3 ║
    ║   1 ║            6 ║
    ║   3 ║            7 ║
    ║   5 ║            4 ║
    ╚═════╩══════════════╝
    :param sample_size:
    :return: X_train, X_test, y_train, y_test, X_encoders[], y_encoder
    """
    Xy = _get_log_useful_cols(sample_size)
    Xy["detection"] = Xy["detection"].apply(lambda x: x / np.timedelta64(1,'s'))
    # "SubLocation" "Direction", "Location", "Lane", "Source", "duration", "detection"
    feature_set_cols = ["SubLocation","Direction", "Location", "Lane", "detection"]
    label_set_cols = ["Category"]
    categorical = ["SubLocation","Direction", "Location", "Lane", "Source"]

    # Textual --> Numerical Categories
    label_encoders = {}
    for column_name in categorical:
        le = LabelEncoder().fit(Xy[column_name])
        Xy[column_name] = le.transform(Xy[column_name])
        label_encoders[column_name] = le

    X = Xy[feature_set_cols]
    print(X.describe())
    y = Xy["Category"].fillna("Information")

    y_encoder = LabelEncoder().fit(y)
    print(y_encoder.classes_)
    y_encoded = DataFrame(y_encoder.transform(y))

    return X, y_encoded, label_encoders, y_encoder

def get_breakdown_xy(sample_size):
    db_wrapper = AutoBMSWrapper()
    session = db_wrapper.session
    query = session.query(
        Breakdown.BreakdownsID, Breakdown.LogID, Breakdown.Reason,
        Breakdown.VehicleType) \
        .order_by(func.RAND()).limit(sample_size).all()
    session.close()
    return DataFrame.from_dict(query)


def get_breakdown_xysplit(Xy:DataFrame):
    """
    :param Xy:
    :return: None (method is a stub)
    """
    return None

if __name__ == "__main__":
    print(get_normal_encoded_x_bin_enc_y(50))
