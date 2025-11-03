import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Page setup
st.set_page_config(page_title="💦 Water Usage Analyzer + Bill Estimator", layout="wide")

# Custom style
st.markdown("""
<style>
    .main {
        background: linear-gradient(to right, #f0f8ff, #e0f7fa);
    }
    .title-text {
        text-align: center;
        font-size: 36px;
        font-weight: 700;
        color: #0077b6;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='title-text'>💧 Water Usage Analyzer & Bill Estimator</h1>", unsafe_allow_html=True)
st.markdown("Analyze, visualize, and predict water usage patterns with smart insights ⚙️")

# Sidebar
st.sidebar.header("📂 Upload or Use Default Data")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

# Load dataset logic
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ File uploaded successfully!")
    st.sidebar.write(f"**File name:** {uploaded_file.name}")
else:
    st.sidebar.info("Using default dataset: `water_usage.csv`")
    df = pd.read_csv("data/water_usage.csv")

# Sidebar navigation
section = st.sidebar.radio("🔍 Navigate", ["Overview", "Trends & Analysis", "Prediction", "Custom Bill"])

# ----- Overview -----
if section == "Overview":
    st.subheader("📊 Dataset Overview")
    st.dataframe(df.head())

    col1, col2, col3 = st.columns(3)
    avg_usage = df["Water_Usage_Liters"].mean()
    total_usage = df["Water_Usage_Liters"].sum()
    avg_bill = df["Bill_Amount"].mean()

    col1.metric("💧 Average Usage (L)", f"{avg_usage:.2f}")
    col2.metric("💰 Average Bill (₹)", f"{avg_bill:.2f}")
    col3.metric("📦 Total Usage (L)", f"{total_usage:.2f}")

# ----- Trends & Analysis -----
elif section == "Trends & Analysis":
    st.subheader("📈 Water Usage & Bill Trends")

    required = ["Month", "Household", "Water_Usage_Liters", "Bill_Amount"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Missing columns in CSV: {missing}. Required: {required}")
    else:
        # Convert and sort
        df["Water_Usage_Liters"] = pd.to_numeric(df["Water_Usage_Liters"], errors="coerce")
        df["Bill_Amount"] = pd.to_numeric(df["Bill_Amount"], errors="coerce")

        month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        if df["Month"].isin(month_order).all():
            df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)

        houses = df["Household"].unique()
        selected_house = st.selectbox("🏠 Select Household", houses)
        house_data = df[df["Household"] == selected_house].sort_values("Month")

        # Plot
        fig, ax1 = plt.subplots(figsize=(9, 4))
        months = house_data["Month"].astype(str).tolist()

        ax1.plot(months, house_data["Water_Usage_Liters"], color="#0077b6", marker="o",
                 linewidth=2.5, label="Usage (L)", zorder=3)
        ax1.set_xlabel("Month")
        ax1.set_ylabel("Usage (L)", color="#0077b6")
        ax1.tick_params(axis='y', labelcolor="#0077b6")

        ax2 = ax1.twinx()
        ax2.plot(months, house_data["Bill_Amount"], color="#ef476f", marker="s",
                 linewidth=2.0, linestyle="--", label="Bill (₹)", zorder=2)
        ax2.set_ylabel("Bill (₹)", color="#ef476f")
        ax2.tick_params(axis='y', labelcolor="#ef476f")

        # Adjust axis limits for better visibility
        ax1.set_ylim(0, max(house_data["Water_Usage_Liters"]) * 1.2)
        ax2.set_ylim(0, max(house_data["Bill_Amount"]) * 1.2)

        plt.xticks(rotation=30)
        ax1.set_title(f"Monthly Usage vs Bill — Household {selected_house}")

        lines_1, labels_1 = ax1.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left")

        st.pyplot(fig)
        st.markdown("💡 **Insight:** Peaks in water usage directly increase the bill — check months with higher usage.")

# ----- Prediction -----
elif section == "Prediction":
    st.subheader("🔮 Predict Future Bill (using Linear Regression)")

    X = df[["Water_Usage_Liters"]]
    y = df["Bill_Amount"]
    model = LinearRegression()
    model.fit(X, y)

    usage_input = st.number_input("Enter expected next month's water usage (Liters):", min_value=100, max_value=5000, step=50)
    if usage_input:
        predicted_bill = model.predict([[usage_input]])[0]
        st.success(f"💰 Estimated Bill: ₹{predicted_bill:.2f}")
        st.markdown("🧠 Model trained using past data (Usage vs Bill) to predict next month’s charges.")

# ----- Custom Bill -----
elif section == "Custom Bill":
    st.subheader("💧 Custom Bill Estimation")

    usage = st.number_input("Enter expected water usage (Liters):", min_value=100, max_value=5000, step=50, value=1000)
    rate = st.slider("Set rate per liter (₹)", 0.1, 2.0, 0.6)
    estimated_bill = usage * rate
    st.success(f"💰 Estimated Bill: ₹{estimated_bill:.2f}")

    save_percent = st.slider("Water saving target (%)", 5, 50, 10)
    saved_usage = usage * (1 - save_percent / 100)
    saved_bill = saved_usage * rate
    savings = estimated_bill - saved_bill

    col1, col2, col3 = st.columns(3)
    col1.metric("🚿 Current Usage", f"{usage} L")
    col2.metric("💧 After Saving", f"{saved_usage:.0f} L")
    col3.metric("💸 Bill Savings", f"₹{savings:.2f}")

    st.markdown(f"🌿 If you save **{save_percent}% water**, you’ll reduce your bill by **₹{savings:.2f}** this month!")
