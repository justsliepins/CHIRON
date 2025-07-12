# ⚡ CHIRON: Smart EV Charging with Reinforcement Learning

> **"Chiron"** — named after the wise centaur of Greek mythology — guides intelligent decision-making for smart electric vehicle (EV) charging.

---

## 🚗 Project Overview

CHIRON is a reinforcement learning-based smart charging algorithm designed for electric vehicles. It aims to:

- ⚡ **Minimize electricity costs** by adapting to real-time market prices.
- 🧠 **Preserve battery health** by avoiding harmful charge patterns.
- 🕒 **Guarantee timely full charge** before scheduled departure.

The system operates in two intelligent modes:

- 🔌 **Grid-to-Vehicle (G2V)**: Charge the EV when electricity is cheapest.
- 🔋 **Vehicle-to-Grid (V2G)**: Sell electricity back to the grid during peak prices, while ensuring the EV reaches the required State of Charge (SOC) before departure.

---

## 🧠 Reinforcement Learning Framework

CHIRON uses a **Markov Decision Process (MDP)** and is trained using reinforcement learning to learn the optimal charging strategy.

### 🧩 Environment Includes:

- **State Space**: SOC, time step index, battery SOH, and electricity price.
- **Action Space**: Discrete charging rates `[-6, -4, -2, 0, 2, 4, 6]` kW.
- **Reward Function**:
  - Penalizes electricity cost and battery degradation.
  - Adds a penalty if SOC is not met by the end of the charging window.

---

## 🛠️ Key Components

- 🔋 **Battery Model**: Tracks SOC, models energy flow and internal losses.
- ⏱️ **Time Model**: Discretized charging window (e.g., 5, 10, 15 min steps).
- 💔 **Degradation Model**: Models calendar and cyclic aging effects.
- 💸 **Market Prices**: Loads historical/real-time electricity prices from external data.

---

## 🔁 Training Process

1. **Build the simulation environment** (custom Gym environment).
2. **Define states, actions, and rewards**.
3. **Train with RL algorithm** (e.g., Q-Learning or DQN via Stable-Baselines3).
4. **Evaluate against baselines** ("Dumb" or "Mean" charging strategies).

---

## 📈 Evaluation & Visualization

- Visual comparison of strategies using SOC curves, charging rates, and cost plots.
- Compare total cost, battery wear, and performance of different agents.

---

## 🚀 Deployment

CHIRON can be integrated into real-time applications:

- 🧩 **Python API**: For training and inference.
- 🌐 **Flask/FastAPI service**: For integration with .NET/C# systems.
- 🔄 **Real-time decision loop**: Make decisions every 5–15 minutes during a charging window.

---

## 📎 Future Enhancements

- Support for **variable C-rates** and **multi-vehicle scheduling**.
- Incorporate **predictive electricity price models**.
- Add **real-world battery diagnostics integration**.

---

## 🧾 Source & Inspiration

Inspired by academic research on battery-aware charging with reinforcement learning. See project discussions and papers in `/docs` folder.

---

> Smart charging. Mythic wisdom. Maximum efficiency. — **CHIRON**

