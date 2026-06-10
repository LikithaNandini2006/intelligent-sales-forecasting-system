from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from utils.preprocess import load_sales_data


MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "sales_model.pkl"


def train_sales_model():
    df = load_sales_data()
    features = df[["unit_price", "stock"]]
    target = df["units_sold"]
    x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.25, random_state=42)
    model = RandomForestRegressor(n_estimators=80, random_state=42)
    model.fit(x_train, y_train)
    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model, model.score(x_test, y_test)


if __name__ == "__main__":
    trained_model, score = train_sales_model()
    print(f"Saved {trained_model.__class__.__name__} to {MODEL_PATH} with R2 score {score:.2f}")
