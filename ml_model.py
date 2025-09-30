import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer


MODEL_PATH = "model.pkl"
SCALER_PATH = "scaler.pkl"
IMPUTER_PATH = "imputer.pkl"


def prepare_data(df: pd.DataFrame):
    """
    Splits DataFrame into features (X) and target (y).
    For this example, let's predict employee_age.
    """
    X = df[["employee_degree", "employee_experience", "department_id"]]
    y = df["employee_age"]
    return X, y


def train_model(df: pd.DataFrame):
    X, y = prepare_data(df)


    imputer = SimpleImputer(strategy="mean")
    X = imputer.fit_transform(X)


    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )


    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)


    model = LinearRegression()
    model.fit(X_train_scaled, y_train)


    joblib.dump(model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(imputer, IMPUTER_PATH)


    loss = model.score(X_test_scaled, y_test)
    return model, loss


def load_trained_model():
    if not (
        os.path.exists(MODEL_PATH)
        and os.path.exists(SCALER_PATH)
        and os.path.exists(IMPUTER_PATH)
    ):
        return None, None, None
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    imputer = joblib.load(IMPUTER_PATH)
    return model, scaler, imputer


def predict(model, scaler, imputer, X: pd.DataFrame):
    """
    Make predictions with preprocessing (impute + scale).
    """
    X_imputed = imputer.transform(X)
    X_scaled = scaler.transform(X_imputed)
    return model.predict(X_scaled)
