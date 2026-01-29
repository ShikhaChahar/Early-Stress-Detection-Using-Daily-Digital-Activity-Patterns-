# 📘 Early Stress Detection Using Daily Digital Activity Patterns

## Project Overview
This project implements a **machine learning–based early stress detection system** using **daily digital activity patterns** derived from smartphone usage behavior.  
The goal is to identify **early behavioral indicators of stress** before it manifests into severe psychological or physiological symptoms.

Unlike traditional stress detection approaches that rely on **wearable sensors or self-reported surveys**, this system leverages **passively collected digital behavior data**, making it scalable, non-intrusive, and privacy-aware.

> ⚠️ **Ownership Notice:**  
> This project and its research concept belong to **Shikha Chahar**.  
> The implementation is based on her academic research work.

---

## 👩‍🎓 Author
**Shikha Chahar**  
Department of Computer Science Engineering  
Apex Institute of Technology  
Chandigarh University, Punjab, India  

---

## 🎯 Objectives
- Detect early stress signals using **digital behavior patterns**
- Model stress as a **progressive risk score**, not just a binary outcome
- Ensure **interpretability** through feature importance analysis
- Design a **modular and reproducible ML pipeline**

---

## 📊 Dataset
Due to privacy and accessibility constraints of raw smartphone sensing datasets, this project uses a **synthetically generated dataset** that simulates realistic daily digital behavior of students.

### Features Used
| Feature | Description |
|------|------------|
| screen_time | Total screen usage per day (minutes) |
| app_sessions | Number of application launches |
| night_usage | Screen usage between 12 AM – 5 AM |
| call_count | Number of phone calls |
| sms_count | Number of SMS messages |
| sleep_hours | Estimated sleep duration |
| app_entropy | App usage diversity |
| screen_per_session | Average screen time per session |
| night_screen_ratio | Ratio of night usage to total screen time |
| sleep_deficit | Deviation from ideal sleep duration |

**Target Variable**
- stress_label  
  - 0 → Low Stress  
  - 1 → High Stress  

---

## 🧠 Methodology
1. **Feature Engineering**  
   Behavioral ratios and sleep-related indicators are derived to capture subtle stress signals.

2. **Model Architecture**  
   - Gradient Boosting Classifier  
   - Feature scaling using StandardScaler  
   - Stratified train–test split  

3. **Evaluation Strategy**
   - Precision, Recall, F1-Score  
   - ROC–AUC Curve  
   - Feature Importance Visualization  

4. **Risk-Based Output**
   - Continuous **Stress Risk Score (0–1)** generated using prediction probabilities  
   - Enables early-warning and graded intervention strategies

---

## 📈 Key Results
- The model demonstrates reliable discrimination between low-stress and high-stress behavioral patterns.
- Night-time smartphone usage, sleep deficit, and behavioral fragmentation are identified as strong stress indicators.
- Continuous stress risk scores support **early detection** rather than reactive classification.

---

## 📂 Project Structure
```
Stress Detection/
│
├── train_model.py
├── evaluate.py
├── graphs.py
├── feature_engineering.py
├── artifacts/
│   ├── model.pkl
│   ├── features.pkl
│   └── y_prob.npy
└── synthetic_studentlife_stress_data.csv
```

---

## ▶️ How to Run

### Step 1: Train the model
```bash
python train_model.py
```

### Step 2: Evaluate performance
```bash
python evaluate.py
```

### Step 3: Generate visualizations
```bash
python graphs.py
```

---

## ⚖️ Ethical & Usage Disclaimer
- The system is **not a clinical diagnostic tool**
- Stress predictions represent **behavioral risk indicators**
- Synthetic data is used for experimental validation only
- Designed with **privacy-preserving principles**

---

## 🔮 Future Enhancements
- Temporal stress progression modeling
- Personalized baseline adaptation
- Federated learning for privacy-aware deployment
- Integration with real-world smartphone sensing data
- Intervention effectiveness modeling

---

## 📌 Acknowledgement
This implementation is based on the original research work of **Shikha Chahar** and is intended strictly for **academic and research purposes**.
