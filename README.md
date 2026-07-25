# 🏏 IPL InsightXI — IPL Analytics Dashboard & Match Prediction System

**IPL InsightXI** is an interactive cricket analytics platform built with Python and Streamlit. It analyzes historical IPL data to deliver team performance insights, player statistics, venue intelligence, and a machine learning–powered match winner prediction engine — all through a clean, interactive web dashboard.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Machine Learning Workflow](#-machine-learning-workflow)
- [Dataset](#-dataset)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Model Details](#-model-details)
- [Screenshots](#-screenshots)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 Overview

IPL InsightXI combines exploratory data analysis, feature engineering, and a trained Random Forest Classifier to help users explore IPL history and predict match outcomes. The platform is designed for cricket fans, analysts, and data science enthusiasts who want an intuitive way to explore over a decade of IPL data.

---

## ✨ Features

### 🏆 Match Prediction
- Predicts the IPL match winner using a trained Random Forest model
- User selects two teams, toss winner, venue, and season
- Displays predicted winner along with model confidence score

### 📊 Team Analysis
- Team performance overview
- Win/loss statistics
- Season-wise performance trends
- Historical head-to-head team comparison

### 🧑‍🤝‍🧑 Player Statistics
- Individual player performance analysis
- Batting statistics (runs, strike rate, averages, etc.)
- Bowling statistics (wickets, economy, averages, etc.)

### 🏟️ Venue Analysis
- Venue-based match insights
- Match distribution across stadiums
- Scoring pattern analysis by venue

---

## 🛠️ Tech Stack

| Category            | Tools/Libraries              |
|---------------------|-------------------------------|
| Language             | Python                        |
| Data Handling        | Pandas, NumPy                 |
| Machine Learning      | Scikit-learn, Random Forest Classifier |
| Web App Framework     | Streamlit                     |
| Visualization         | Plotly, Matplotlib            |
| Model Persistence     | Joblib                        |

---

## 🔄 Machine Learning Workflow

```
Data Collection → Data Cleaning → Exploratory Data Analysis 
→ Feature Engineering → Model Training → Model Evaluation → Deployment (Streamlit)
```

1. **Data Collection** — Gathered historical IPL match and ball-by-ball data
2. **Data Cleaning** — Handled missing values, standardized team/venue names, removed inconsistencies
3. **Exploratory Data Analysis (EDA)** — Analyzed trends in team performance, toss impact, venue behavior, and player stats
4. **Feature Engineering** — Derived features such as team win percentages, toss advantage, venue-based stats, and head-to-head records
5. **Model Training** — Trained a Random Forest Classifier on engineered features
6. **Model Evaluation** — Evaluated using accuracy, precision, recall, and cross-validation
7. **Deployment** — Deployed the trained model in an interactive Streamlit web application

---

## 📁 Dataset

The project uses IPL historical data, including:

- **Match Information** — match ID, date, season, result
- **Teams** — participating teams for each match
- **Toss Details** — toss winner and toss decision
- **Venue** — stadium and city information
- **Winners** — match winner and margin of victory
- **Ball-by-Ball Delivery Data** — detailed delivery-level data for batting and bowling statistics

> **Note:** Dataset source/link can be added here (e.g., Kaggle IPL dataset).

---

## 📂 Project Structure

```
IPL-InsightXI/
│
├── data/
│   ├── matches.csv
│   └── deliveries.csv
│
├── models/
│   └── match_winner_model.pkl
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
│   └── 03_model_training.ipynb
│
├── src/
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   └── train_model.py
│
├── app.py
├── requirements.txt
└── README.md
```

> Update this structure to match your actual repository layout.

---

# 📸 Application Preview

## 🏠 Home Dashboard

![Home Dashboard](screenshots/homepage_1.1.png)

---

## 🎯 Match Prediction

### Prediction Interface
![Prediction Interface](screenshots/match_prediction_2.1.png)

### Team Selection
![Team Selection](screenshots/match_prediction_2.2.png)

### Prediction Result
![Prediction Result](screenshots/match_prediction_2.3.png)

---

## 📊 Team Analysis

### Team Overview
![Team Overview](screenshots/team_analyis_3.1.png)

### Team Performance
![Team Performance](screenshots/team_analyis_3.2.png)

---

## 🏏 Player Statistics

### Player Dashboard
![Player Dashboard](screenshots/player_statistics_4.1.png)

### Batting Analysis
![Batting Analysis](screenshots/player_statistics_4.2.png)

### Top Run Scorers
![Top Run Scorers](screenshots/player_statistics_4.3.png)

### Strike Rate Analysis
![Strike Rate Analysis](screenshots/player_statistics_4.4.png)

### Bowling Analysis
![Bowling Analysis](screenshots/player_statistics_4.5.png)

### Top Wicket Takers
![Top Wicket Takers](screenshots/player_statistics_4.6.png)

### Player Insights
![Player Insights](screenshots/player_statistics_4.7.png)

---

## 📍 Venue Analysis

### Venue Dashboard
![Venue Dashboard](screenshots/venue_analysis_5.1.png)

### Venue Statistics
![Venue Statistics](screenshots/venue_analysis_5.2.png)

### Venue Comparison
![Venue Comparison](screenshots/venue_analysis_5.3.png)

### Scoring Pattern
![Scoring Pattern](screenshots/venue_analysis_5.4.png)

### Win Analysis
![Win Analysis](screenshots/venue_analysis_5.5.png)

### Venue Insights
![Venue Insights](screenshots/venue_analysis_5.6.png)

### Additional Analysis
![Additional Analysis](screenshots/venue_analysis_5.7.png)

### More Insights
![More Insights](screenshots/venue_analysis_5.8.png)

### Final Dashboard
![Final Dashboard](screenshots/venue_analysis_5.9.png)


## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/IPL-InsightXI.git
   cd IPL-InsightXI
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

Then open your browser and navigate to:

```
http://localhost:8501
```

### Using the App
1. Select the **Match Prediction** tab to predict a winner
2. Choose two teams, toss winner, venue, and season
3. Click **Predict** to view the predicted winner and confidence score
4. Explore **Team Analysis**, **Player Statistics**, and **Venue Analysis** tabs for deeper insights

---

## 🤖 Model Details

- **Algorithm:** Random Forest Classifier
- **Input Features:** Team stats, toss winner, toss decision, venue, season, historical head-to-head performance
- **Output:** Predicted match winner with confidence score
- **Persistence:** Model saved and loaded using `joblib`

```python
import joblib

model = joblib.load("models/match_winner_model.pkl")
prediction = model.predict(input_features)
```

---

## 🖼️ Screenshots

> Add screenshots or GIFs of your dashboard here to showcase the UI.

```
[Match Prediction Screenshot]
[Team Analysis Screenshot]
[Player Statistics Screenshot]
[Venue Analysis Screenshot]
```

---

## 🚀 Future Improvements

- Add live match data integration via API
- Incorporate player form and injury data for better predictions
- Add advanced models (XGBoost, LightGBM) for comparison
- Implement win probability graphs during live matches
- Add fantasy team recommendation feature

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m "Add your feature"`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

### 👤 Author

**Your Name**
[GitHub](https://github.com/ompatell18) • [LinkedIn](https://linkedin.com/in/om-patel-6107b0411)

---

⭐ If you found this project useful, consider giving it a star on GitHub!
