# 💧 Water Usage Analyzer & Bill Estimator

An interactive Streamlit app that analyzes household water usage and estimates bills.  
Upload your own CSV dataset or use the sample provided to visualize and predict usage trends.

---

## 1️⃣ **Clone the Repository**

```bash
git clone https://github.com/r20j/water-usage-analyzer.git
cd water-usage-analyzer
```

---

## 2️⃣ **Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## 3️⃣ **Run the App**

```bash
streamlit run app.py
```

---

## 🧾 Example Dataset

You can use your own CSV or the included sample (`test_water_data.csv`).

**Example data format:**

```csv
Month,Household,Water_Usage_Liters,Bill_Amount
Jan,A,1200,240
Feb,A,1300,260
Mar,A,1250,250
Apr,A,1350,270
```

---

## 🧠 Tech Stack

| Technology | Role |
|-------------|------|
| 🐍 Python | Core programming language |
| 🌐 Streamlit | Web app framework |
| 📊 Matplotlib | Data visualization |
| 📋 Pandas | Data handling |
| 🧮 NumPy | Numerical operations |
| 🤖 Scikit-Learn | Regression model for bill prediction |

---

## 💻 Features

✅ Upload your own `.csv` dataset  
✅ Visualize monthly water usage per household  
✅ Compare actual vs predicted bills  
✅ Apply percentage-based water saving scenarios  
✅ Download modified dataset as `.csv`

---

## 📂 Project Structure

```bash
water-usage-analyzer/
│
├── app.py
├── requirements.txt
├── test_water_data.csv
└── README.md
```

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---


