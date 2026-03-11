import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor


models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(),
    "Lasso Regression": Lasso(),
    "Decision Tree": DecisionTreeRegressor(),
    "Random Forest": RandomForestRegressor()
}

def run_model(request, path):

    df = pd.read_csv(path)
    df = df[df["actividad"] == request.activity]

    print(df)
    X = df["tiempo"].values.reshape(-1, 1)
    y = df["fc"].values

    model = LinearRegression()
    model.fit(X, y)

    predictions = model.predict(X)

    equation = f"y = {model.intercept_:.2f} + {model.coef_[0]:.2f}x"

    return {
        "equation": equation,
        "results": {
            "real_values": y.tolist(),
            "predicted_values": predictions.tolist(),
            "time_points": X.flatten().tolist()
        },
        "metrics": {
            "r2_score": model.score(X, y)
        }
    }