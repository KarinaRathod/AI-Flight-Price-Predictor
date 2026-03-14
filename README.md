
# ✈️ AI Flight Price Predictor

An AI-powered web application built with Streamlit that predicts flight ticket prices based on various parameters like airline, source, destination, departure time, and how far in advance you book.

## ✨ Features
* **Predictive Pricing:** Estimates flight fares using a pre-trained Machine Learning model.
* **Dynamic Price Trend:** Visualizes how prices might fluctuate over a 30-day booking window.
* **Modern UI:** Clean, interactive, and responsive dashboard built entirely in Python.

## 📂 Project Structure
* `app.py`: The main Streamlit application code.
* `flight_model.pkl`: The trained Machine Learning model.
* `encoders.pkl`: The label encoders used to process categorical text inputs into numbers.
* `requirements.txt`: The list of Python dependencies required to run the app.

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd <your-repo-folder-name>

```

2. **Create a virtual environment (Recommended):**
```bash
python -m venv venv

# Activate on Mac/Linux:
source venv/bin/activate  

# Activate on Windows:
venv\Scripts\activate

```


3. **Install the dependencies:**
```bash
pip install -r requirements.txt

```


4. **Run the Streamlit app:**
```bash
streamlit run app.py

```

