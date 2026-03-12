import pandas as pd
import numpy as np
import time
from typing import Any

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor

from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

models = {
    "ridge": Ridge(),
    "lasso": Lasso(),
    "decision_tree": DecisionTreeRegressor(),
    "random_forest": RandomForestRegressor(),
    "knn": KNeighborsRegressor(n_neighbors=5),
    "svr": SVR(kernel="rbf"),
    "gradient_boosting": GradientBoostingRegressor(),
    "neural_network": Pipeline([
        ("scaler", StandardScaler()),
        ("mlp", MLPRegressor(
            hidden_layer_sizes=(30,20),
            activation="relu",
            max_iter=5000,
            random_state=42
        ))
    ])
}

SUPPORTED_ALGORITHMS = ["polynomial", *models.keys()]


def _build_model(algorithm: str, degree: int):
    if algorithm == "polynomial":
        return Pipeline([
            ("poly", PolynomialFeatures(degree=degree)),
            ("linear", LinearRegression())
        ])

    if algorithm not in models:
        raise ValueError(f"Algoritmo '{algorithm}' no soportado")

    return models[algorithm]


def _format_linear_equation(intercept: float, coef: float) -> str:
    sign = "+" if coef >= 0 else "-"
    return f"y = {intercept:.4f} {sign} {abs(coef):.4f}x"


def _format_polynomial_equation(model: Pipeline) -> str:
    linear_model = model.named_steps["linear"]
    poly = model.named_steps["poly"]

    feature_names = poly.get_feature_names_out(["x"])
    coefficients = linear_model.coef_
    intercept = linear_model.intercept_

    terms = [f"{intercept:.4f}"]
    for feature_name, coef in zip(feature_names, coefficients):
        if feature_name == "1" or abs(coef) < 1e-10:
            continue

        sign = "+" if coef >= 0 else "-"
        human_feature = feature_name.replace("^", "^")
        terms.append(f"{sign} {abs(coef):.4f}{human_feature}")

    return "y = " + " ".join(terms)


def _get_equation(model: Any, algorithm: str) -> str | None:
    if algorithm == "polynomial" and isinstance(model, Pipeline):
        return _format_polynomial_equation(model)

    if algorithm in {"ridge", "lasso"}:
        intercept = float(model.intercept_)
        coef = float(np.ravel(model.coef_)[0])
        return _format_linear_equation(intercept, coef)

    return None


def _run_algorithm(algorithm: str, degree: int, X, y):
    model = _build_model(algorithm, degree)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    time_start = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - time_start

    pred_test = model.predict(X_test)
    predictions = model.predict(X)

    mae = mean_absolute_error(y_test, pred_test)
    mse = mean_squared_error(y_test, pred_test)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, pred_test)

    return {
        "algorithm": algorithm,
        "training_time": training_time,
        "degree": degree if algorithm == "polynomial" else None,
        "equation": _get_equation(model, algorithm),
        "results": {
            "real_values": y.tolist(),
            "predicted_values": predictions.tolist(),
            "time_points": X.flatten().tolist()
        },
        "metrics": {
            "mae": mae,
            "mse": mse,
            "rmse": rmse,
            "r2_score": r2
        }
    }


def _load_dataset(path, activity: str):
    df = pd.read_csv(path)
    df = df[df["actividad"] == activity]

    if df.empty:
        raise ValueError("No hay datos para la actividad seleccionada")

    X = df["tiempo"].values.reshape(-1, 1)
    y = df["fc"].values
    return X, y

def run_model(request, path):
    degree = request.degree or 2
    X, y = _load_dataset(path, request.activity)
    return _run_algorithm(request.model_type, degree, X, y)


def run_models_for_report(path, activity: str, degree: int = 2, algorithms: list[str] | None = None):
    selected_algorithms = algorithms or SUPPORTED_ALGORITHMS
    X, y = _load_dataset(path, activity)

    results = []
    for algorithm in selected_algorithms:
        results.append(_run_algorithm(algorithm, degree, X, y))

    return results