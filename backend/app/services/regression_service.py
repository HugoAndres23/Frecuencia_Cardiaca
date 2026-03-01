import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def run_model(request):

    path = f"app/data/{request.filename}"
    df = pd.read_csv(path)

    df = df[df["actividad"] == request.activity]

    X = df["tiempo"].values.reshape(-1, 1)
    y = df["fc"].values

    model = LinearRegression()
    model.fit(X, y)

    predictions = model.predict(X)

    equation = f"y = {model.intercept_:.2f} + {model.coef_[0]:.2f}x"

    return {
        "equation": equation,
        "real_values": y.tolist(),
        "predicted_values": predictions.tolist()
    }