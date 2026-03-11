import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor


models = {
    "linear_regression": LinearRegression(),
    "decision_tree": DecisionTreeRegressor(),
    "random_forest": RandomForestRegressor()
}

def run_model(request, path):

    df = pd.read_csv(path)
    # df = df[df["actividad"] == request.activity]
    X = df["tiempo"].values.reshape(-1, 1)
    y = df["fc"].values
    print(f"Ejecutando modelo: {request.model_type} para la actividad: {request.activity}")
    model = models.get(request.model_type, None)

    if model is None:
        return {"error": "Modelo no soportado"}
    
    model.fit(X, y)

    predictions = model.predict(X)

    return {
        "results": {
            "real_values": y.tolist(),
            "predicted_values": predictions.tolist(),
            "time_points": X.flatten().tolist()
        },
        "metrics": {
            "r2_score": model.score(X, y),
            "mae": np.mean(np.abs(y - predictions)),
            "mse": np.mean((y - predictions) ** 2)
        }
    }