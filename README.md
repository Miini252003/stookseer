#  📈 StockSeer — Hybrid CNN-LSTM Real-Time Stock Price Prediction

> 📰 **Published Research Paper**
> International Journal of Advanced Multidisciplinary Research and Educational Development (IJAMRED)
> Volume 2, Issue 2 | March–April 2026 | ISSN: 3107-6513

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat&logo=python)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?style=flat&logo=tensorflow)](https://tensorflow.org)
[![Flask](https://img.shields.io/badge/Flask-REST_API-black?style=flat&logo=flask)](https://flask.palletsprojects.com)
[![Deployed on Render](https://img.shields.io/badge/Deployed-Render-46E3B7?style=flat&logo=render)](https://render.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

---

## 🧠 Overview

**StockSeer** is a hybrid deep learning framework that combines:
- **CNN** (Convolutional Neural Network) for short-term feature extraction
- **LSTM** (Long Short-Term Memory) for long-term sequential modeling

It predicts stock prices in real-time with a Flask-based interactive web dashboard, tested on **12 stocks across NSE and NASDAQ** using 5 years of historical data.

---

## 🏆 Results

| Model | Directional Accuracy | MAPE |
|---|---|---|
| **CNN-LSTM (StockSeer)** | **74.3%** | **2.1%** |
| LSTM (baseline) | 66.1% | 2.9% |
| ARIMA (baseline) | 58.4% | 2.9% |

> ✅ CNN-LSTM reduces prediction error by approximately **$3.20 per share** on a $400 stock compared to baselines.

---

## 🏗️ Model Architecture

```
Input Data (OHLCV + Indicators)
        │
        ▼
┌─────────────────────┐
│  CNN Layer 1        │  ← 64 filters, kernel size 3, ReLU
│  CNN Layer 2        │  ← 64 filters, kernel size 3, ReLU
│  MaxPooling         │  ← Dimensionality reduction
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  LSTM Layer 1       │  ← 128 units
│  LSTM Layer 2       │  ← 64 units
│  Dropout (0.2)      │  ← Prevent overfitting
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Fusion Layer       │  ← Feature merge
│  Dense Output       │  ← Price + Confidence interval
└─────────────────────┘
```

---

## 📊 Input Features

| Feature | Description |
|---|---|
| OHLCV | Open, High, Low, Close, Volume |
| RSI | 14-day Relative Strength Index |
| Bollinger Bands | 20-day Bollinger Band Width |
| SMA | Simple Moving Average |
| EMA | Exponential Moving Average |

- **Lookback Window:** 60 days
- **Forecast Horizons:** 1, 7, 14, 30, 60 days
- **Normalization:** Min-Max Scaling

---

## ⚙️ Training Strategy

| Parameter | Value |
|---|---|
| Optimizer | Adam (lr = 0.001) |
| Loss Function | Huber Loss |
| Regularization | Dropout (0.2) |
| Early Stopping | ✅ Enabled |
| LR Scheduling | ✅ Enabled |
| Train/Val/Test Split | 80 / 10 / 10 |

### Uncertainty Estimation
Confidence intervals computed as:

```
CIₖ = p̂ₖ ± 1.5σ√k
```
where σ is volatility from past returns — accounts for increasing uncertainty over longer horizons.

---

## 🌐 System Features

### Backend (Flask REST API)
| Endpoint | Function |
|---|---|
| `/login`, `/register` | User authentication (SHA-256) |
| `/history`, `/live` | Historical & live stock data |
| `/predict`, `/compare` | Predictions & stock comparison |

### Data Pipeline
- Real-time stock data via **yfinance** (updates every 5 seconds)
- RSI, Bollinger Bands, SMA, EMA computed dynamically using NumPy

### Frontend
- Vanilla JavaScript SPA with **Chart.js**
- Real-time dashboard with predictions + confidence intervals
- Stock comparison feature

### Deployment
- Deployed on **Render** (Python 3.12 + Gunicorn)
- **GitHub CI/CD** pipeline for automated deployment

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.12 |
| Deep Learning | TensorFlow, Keras |
| Data Processing | NumPy, Pandas, yfinance |
| Web Framework | Flask |
| Frontend | Vanilla JS, Chart.js, CSS |
| Deployment | Render, Gunicorn |
| CI/CD | GitHub Actions |
| Security | SHA-256 hashing, session cookies |

---

## 📁 Project Structure

```
stookseer/
│
├── app.py                  ← Flask entry point
├── requirements.txt        ← Python dependencies
├── config/                 ← Configuration settings
├── model/
│   ├── cnn_lstm.py         ← Hybrid model definition
│   ├── train.py            ← Training script
│   └── predict.py          ← Inference script
├── pipeline/
│   ├── data_fetch.py       ← yfinance data pipeline
│   ├── indicators.py       ← RSI, BB, SMA, EMA
│   └── preprocess.py       ← Normalization & windowing
├── static/
│   └── style.css           ← Frontend styles
├── templates/
│   ├── index.html          ← Main dashboard
│   └── result.html         ← Prediction results
└── README.md
```

---

## 🚀 Setup & Run

### 1. Clone the Repository
```bash
git clone https://github.com/Miini252003/stookseer.git
cd stookseer
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
python app.py
```

### 5. Open in Browser
```
http://127.0.0.1:5000
```

---

## 📦 Requirements

```
tensorflow>=2.10
flask
numpy
pandas
yfinance
scikit-learn
matplotlib
gunicorn
```

---

## 🔬 Limitations & Future Work

### Current Limitations
- Does not include sentiment or macroeconomic data
- Backtesting ignores real trading costs
- Cold start latency on deployment

### Future Work
- Transformer-based attention models
- Sentiment analysis using NLP
- Reinforcement learning for trading strategies

---

## 📜 Citation

If you use this work, please cite:

```bibtex
@article{rana2026stockseer,
  title     = {StockSeer: A Hybrid CNN-LSTM Framework for Real-time Stock Price Prediction},
  author    = {Rana, Divyanshi and Chaudhary, Harsh and Rasheed, Md. Emamoor},
  journal   = {International Journal of Advanced Multidisciplinary Research and Educational Development},
  volume    = {2},
  number    = {2},
  year      = {2026},
  issn      = {3107-6513}
}
```

---

## 👩‍💻 Authors

| Name | Role |
|---|---|
| **Divyanshi Rana** | Lead Developer & Researcher |
| **Harsh Chaudhary** | Co-Researcher |
| **Md. Emamoor Rasheed** | Co-Researcher |

B.Tech Computer Science & Engineering (AI/ML)
IIMT College of Engineering, Greater Noida, Uttar Pradesh

---

## 📫 Connect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Divyanshi_Rana-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/divyanshi-rana)
[![GitHub](https://img.shields.io/badge/GitHub-Miini252003-181717?style=flat&logo=github)](https://github.com/Miini252003)
[![Email](https://img.shields.io/badge/Email-divyanshirana2004@gmail.com-D14836?style=flat&logo=gmail)](mailto:divyanshirana2004@gmail.com)

---

## ⭐ Star This Repo

If you found this project useful, please consider giving it a ⭐ — it helps others discover the project!
