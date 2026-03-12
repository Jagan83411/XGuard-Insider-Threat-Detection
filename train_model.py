import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pickle

def train_model():
    df = pd.read_csv("employee_logs.csv")

    features = ["login_hour", "files_accessed", "emails_sent", "usb_used", "after_hours"]
    X = df[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42
    )
    model.fit(X_scaled)

    df["anomaly_score"] = model.decision_function(X_scaled)
    df["is_anomaly"] = model.predict(X_scaled)
    df["is_anomaly"] = df["is_anomaly"].map({1: 0, -1: 1})

    score_min = df["anomaly_score"].min()
    score_max = df["anomaly_score"].max()
    df["risk_score"] = 100 * (1 - (df["anomaly_score"] - score_min) / (score_max - score_min))

    pickle.dump(model, open("model.pkl", "wb"))
    pickle.dump(scaler, open("scaler.pkl", "wb"))
    df.to_csv("results.csv", index=False)

    print("✅ Model trained! results.csv created.")
    return df

if __name__ == "__main__":
    train_model()
