# QARC: Hybrid Financial Intelligence System 🛡️📈

![Status](https://img.shields.io/badge/Status-Prototype-orange) ![Python](https://img.shields.io/badge/Python-3.10-blue) ![Edge AI](https://img.shields.io/badge/Intel-OpenVINO-00C7FD)

## 📌 Overview
**QARC** (Quantitative Analysis & Risk Control) is a next-generation "Robo-Advisor" designed to protect retail investors from market anomalies. Unlike standard trading bots, QARC prioritizes **Capital Preservation** using a 3-layer defense system run locally on Edge AI hardware.

## 🚀 Key Features
* **The Profit Engine:** LSTM networks for 60-day trend forecasting.
* **The Safety Shield:** Isolation Forest "Kill Switch" for detecting Pump & Dump schemes.
* **The News Filter:** **Microsoft Phi-3 / FinBERT** (running locally) for real-time sentiment analysis.
* **Voice-to-Trade:** Hands-free portfolio management using speech recognition.
* **Edge Optimized:** Zero-latency inference on **Intel Core Ultra 5 (NPU) & Arc GPU**.

## 🛠️ Tech Stack
* **AI Core:** PyTorch, TensorFlow, Scikit-Learn.
* **LLM Engine:** Microsoft Phi-3 (via Hugging Face / OpenVINO).
* **Frontend:** Streamlit (with Lottie Animations & Plotly).
* **Backend:** Flask API.
* **Data:** Yahoo Finance (yfinance), Google News.

## 📂 Project Structure
```text
QARC-Financial-System/
├── data/               # Raw & Processed Datasets (Git Ignored)
├── notebooks/          # Research & Training Logs (Jupyter/Colab)
├── src/                # Core Logic (LSTM, Anomaly, NLP modules)
├── web_app/            # The QARC Dashboard (Streamlit)
├── assets/             # Animations (Lottie) & CSS
└── requirements.txt    # Dependencies