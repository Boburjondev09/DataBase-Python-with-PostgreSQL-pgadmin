import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib
import os

MODEL_PATH = "linear_model.pkl"

def prepare_data(df: pd.DataFrame):
    X = pd.DataFrame()
    X['id'] = df['id']
    X['name_length'] = df['name'].apply(len)
    X['uppercase_count'] = df['name'].apply(lambda x: sum(1 for c in x if c.isupper()))
    X['space_count'] = df['name'].apply(lambda x: x.count(' '))
    y = df['name'].apply(len)
    return X, y

def train_model(df: pd.DataFrame, test_size=0.2, random_state=42, save_model=True):
    X, y = prepare_data(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    if save_model:
        joblib.dump(model, MODEL_PATH)

    return model, mse

def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

def predict(model, X):
    return model.predict(X)
