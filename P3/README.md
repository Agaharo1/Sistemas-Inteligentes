# 🍃 Vehicle CO2 Emissions Predictor

A Machine Learning project aimed at classifying vehicles into environmental impact categories based on their technical specifications and fuel consumption. Developed for the **Intelligent Systems** course.

## 👥 Authors
* Antonio García Rodrigo
* Daniel Martín del Castillo
* Pol Montero Pons
* David Díaz Gregorio

## 🎯 Project Objective
The main goal was to transform a numerical regression problem (predicting exact CO2 emissions in g/km) into a **classification problem** featuring 7 environmental impact categories. By analyzing technical specs (engine size, cylinders, transmission, fuel type, etc.), this model can automate the environmental labeling of new vehicles without exhaustive physical testing.

## 📊 Dataset & Preprocessing
* **Data Source:** A dataset comprising 7,385 original vehicle records (`co2.csv`). 
* **Data Cleaning:** Extensive Exploratory Data Analysis (EDA) detected 1,103 duplicate rows (14.97% of the dataset), which were removed to prevent training bias. Final dataset: **6,282 valid records**.
* **Feature Engineering:**
  * Dropped redundant or non-predictive columns (`Model`, `Fuel Consumption Comb (mpg)`, and the target numerical variable).
  * Categorized `CO2 Emissions(g/km)` into 7 discrete bins.
  * Applied `OneHotEncoder` to categorical variables, dropping the first category of each group to avoid multicollinearity. Resulted in a final matrix of **91 features**.

## 🧠 Model Training & Evaluation
The dataset was split into 80% for training and 20% for testing. Four representative algorithms were evaluated. 

Tree-based models vastly outperformed linear models, successfully capturing the non-linear relationships and interactions between variables (like engine size, fuel type, and consumption).

### 🏆 Final Ranking

| Rank | Model | Accuracy |
| :---: | :--- | :--- |
| 🥇 | **Decision Tree** | **95.86%** |
| 🥈 | Random Forest | 95.78% |
| 🥉 | K-Nearest Neighbors (KNN) | 90.29% |
| 4 | Logistic Regression | 89.74% |

**Key Findings & Interpretability:**
* The **Decision Tree** proved to be the optimal solution, showing a robust confusion matrix with only 4.14% errors (exclusively between adjacent boundary categories).
* **Feature Importance:** Combined fuel consumption represents **80.54%** of the model's decision weight. This aligns perfectly with the physical reality: more fuel burned equals more CO2 emitted.

## 🛠️ Tech Stack
* **Language:** Python 3
* **Data Processing:** `pandas`, `numpy`
* **Machine Learning API:** `scikit-learn`
* **Data Visualization:** `matplotlib`, `seaborn`

## 🚀 How to Run

1. Clone this repository to your local machine.
2. Ensure you have the required libraries installed:
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn
3. All the info is on the Jupyter Notebook. Just run the notebook cells to reproduce the Exploratory Data Analysis, model training, and custom vehicle predictions.