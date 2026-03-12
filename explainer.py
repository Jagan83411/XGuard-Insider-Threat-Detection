import pandas as pd
import pickle

def explain_alert(employee_name, df, model, scaler):
    features = ["login_hour", "files_accessed", "emails_sent", "usb_used", "after_hours"]

    emp_data = df[df["employee"] == employee_name].tail(10)
    latest = emp_data.iloc[-1]
    risk = emp_data["risk_score"].iloc[-1]

    reasons = []

    avg_files = df[df["employee"] == employee_name]["files_accessed"].mean()
    if latest["files_accessed"] > avg_files * 3:
        reasons.append(f"accessed {int(latest['files_accessed'])} files — {round(latest['files_accessed']/avg_files, 1)}x their normal amount")

    if latest["login_hour"] < 6:
        reasons.append(f"logged in at {int(latest['login_hour'])}:00 AM — unusual login time")

    if latest["usb_used"] == 1:
        reasons.append("connected an external USB device (rare behavior)")

    if latest["after_hours"] == 1:
        reasons.append("was active after office hours")

    if latest["emails_sent"] > 30:
        reasons.append(f"sent {int(latest['emails_sent'])} emails — higher than usual")

    if not reasons:
        reasons.append("showed an unusual combination of behaviors")

    explanation = f"⚠️ {employee_name} has a risk score of {round(risk)}/100.\n"
    explanation += "Suspicious behaviors detected:\n"
    for i, r in enumerate(reasons, 1):
        explanation += f"  {i}. They {r}\n"

    return explanation, round(risk), reasons

if __name__ == "__main__":
    df = pd.read_csv("results.csv")
    model = pickle.load(open("model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))

    top_threat = df.groupby("employee")["risk_score"].max().idxmax()
    explanation, score, reasons = explain_alert(top_threat, df, model, scaler)
    print(explanation)
