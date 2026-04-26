# QARC: Quantitative Analysis & Risk Control 🛡️📈
**A Hybrid Financial Intelligence System & Edge-Native Robo-Advisor**

![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen) ![Python](https://img.shields.io/badge/Python-3.10-blue) ![Edge AI](https://img.shields.io/badge/Accelerated-Intel_OpenVINO-00C7FD) ![Database](https://img.shields.io/badge/Database-Supabase-3ECF8E) ![API](https://img.shields.io/badge/Backend-Flask-black) ![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Executive Summary
**QARC** is a next-generation predictive trading engine designed to bring institutional-grade risk management to retail investors. Unlike standard algorithmic bots that blindly chase momentum, QARC prioritizes **Capital Preservation** using a multi-layered, AI-driven defense system. 

Built for absolute data privacy and high-speed execution, QARC’s cognitive engine is optimized to run locally on Edge AI hardware (Intel Core Ultra NPUs), while persisting its strategic reasoning to a cloud-native vector database.

---

## 🧠 The 3-Layer Defense Architecture

QARC does not rely on a single point of failure. It uses a trifecta of predictive, protective, and analytical AI models:

### 1. The Profit Engine (Deep Quant Forecasting)
* **Architecture:** Long Short-Term Memory (LSTM) Networks (PyTorch/TensorFlow).
* **Function:** Ingests multivariate time-series data (Closing Price, RSI, MACD, Volume) with a 60-day historical lookback window to forecast short-term price action and trend reversals.

### 2. The Safety Shield (Anomaly Detection)
* **Architecture:** Unsupervised `Isolation Forest` & Scikit-Learn.
* **Function:** Acts as an automated "Kill Switch." Analyzes market micro-structure to detect abnormal volume spikes, liquidity traps, and Pump & Dump schemes. If an anomaly is detected, trade execution is instantly halted.

### 3. The Cognitive Agent (Agentic Reasoning & Memory)
* **Architecture:** Llama-3 / Microsoft Phi-3 + FinBERT + Supabase.
* **Function:** Translates raw quantitative output into actionable trading strategies. The Agent evaluates market sentiment and writes its daily strategic reasoning into a persistent cloud database (`ai_memories`), allowing the AI to learn from its past decisions.

---

## 🏗️ System Infrastructure

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Edge Hardware** | Intel Core Ultra (NPU), MSI Prestige | Zero-latency local inference, hardware-accelerated math. |
| **Model Optimizer** | Intel OpenVINO | Compresses and accelerates PyTorch/LLM inference at the edge. |
| **Data Persistence** | Supabase (PostgreSQL), `yfinance` | Cloud storage for historical `market_data` and Agentic state. |
| **Backend Gateway** | Flask API, Python | REST API that connects the local AI engine to the web/frontend. |
| **User Interface** | Streamlit, Plotly | Real-time, interactive data visualization and portfolio dashboard. |

---

## 🗄️ Database Schema (Supabase)
The backend relies on a custom PostgreSQL schema to maintain state and history.

**`market_data` (The Vault):**
```sql
id BIGINT PRIMARY KEY,
date TIMESTAMP WITH TIME ZONE,
close_price DECIMAL,
rsi DECIMAL,
macd DECIMAL,
volume BIGINT
```