import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from explainer import explain_alert
from report import generate_report

st.set_page_config(
    page_title="XGuard - Insider Threat Detection",
    page_icon="🛡️",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("results.csv")
    model = pickle.load(open("model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))
    return df, model, scaler

df, model, scaler = load_data()

st.markdown("""
<div style='background:linear-gradient(90deg,#1F4E79,#2E75B6);
padding:20px;border-radius:10px;margin-bottom:20px;'>
<h1 style='color:white;margin:0;'>🛡️ XGuard</h1>
<p style='color:#BDD7EE;margin:0;'>Explainable AI for Insider Threat Detection
| Team Codex | REVA University</p>
</div>
""", unsafe_allow_html=True)

total_employees = df["employee"].nunique()
threats = df[df["is_anomaly"] == 1]["employee"].nunique()
safe = total_employees - threats
avg_risk = round(df.groupby("employee")["risk_score"].max().mean())

col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Total Employees", total_employees)
col2.metric("🔴 Threats Detected", threats)
col3.metric("🟢 Safe Employees", safe)
col4.metric("📊 Avg Risk Score", f"{avg_risk}/100")

st.markdown("---")

left, right = st.columns([1, 2])

risk_summary = df.groupby("employee")["risk_score"].max().reset_index()
risk_summary.columns = ["Employee", "Max Risk Score"]
risk_summary = risk_summary.sort_values("Max Risk Score", ascending=False)

with left:
    st.subheader("🚨 Employee Risk Rankings")
    st.dataframe(risk_summary, height=400, use_container_width=True)

with right:
    st.subheader("📊 Risk Distribution Chart")
    fig = px.histogram(
        risk_summary, x="Max Risk Score", nbins=20,
        color_discrete_sequence=["#2E75B6"]
    )
    fig.add_vline(x=70, line_dash="dash", line_color="red",
                  annotation_text="High Risk Threshold")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("🔍 Investigate an Employee")

selected_emp = st.selectbox(
    "Select employee to analyze:",
    risk_summary["Employee"].tolist()
)

if selected_emp:
    emp_data = df[df["employee"] == selected_emp]
    explanation, risk_score, reasons = explain_alert(selected_emp, df, model, scaler)

    color = "#FF4444" if risk_score > 70 else "#FFA500" if risk_score > 40 else "#00C851"
    label = "🔴 HIGH RISK" if risk_score > 70 else "🟡 MEDIUM RISK" if risk_score > 40 else "🟢 LOW RISK"

    st.markdown(f"""
    <div style='background:{color};padding:15px;border-radius:8px;color:white;'>
    <h3 style='margin:0'>{label} — {selected_emp}</h3>
    <h2 style='margin:0'>Risk Score: {risk_score}/100</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🤖 AI Explanation")
    st.info(explanation)

    col_a, col_b = st.columns(2)
    with col_a:
        fig2 = px.line(emp_data, x="day", y="files_accessed",
                       title="Files Accessed Per Day",
                       color_discrete_sequence=["#2E75B6"])
        fig2.add_hline(y=emp_data["files_accessed"].mean(),
                       line_dash="dash", line_color="orange",
                       annotation_text="Their Normal Average")
        st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        fig3 = px.line(emp_data, x="day", y="risk_score",
                       title="Risk Score Over Time",
                       color_discrete_sequence=["#FF4444"])
        fig3.add_hline(y=70, line_dash="dash", line_color="red",
                       annotation_text="Danger Zone")
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### 📄 Generate PDF Report")
    if st.button("⬇️ Generate Report", type="primary"):
        filename = generate_report(selected_emp, risk_score, reasons)
        with open(filename, "rb") as f:
            st.download_button(
                label="📥 Download PDF Report",
                data=f,
                file_name=filename,
                mime="application/pdf"
            )
        st.success(f"✅ Report ready for {selected_emp}!")