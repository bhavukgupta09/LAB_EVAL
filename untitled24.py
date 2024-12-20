# -*- coding: utf-8 -*-
"""Untitled24.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1AV8_iAIR2iZUNRF_ycR6JxN80WZNu20s
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

file_path = "/content/Fuel_cell_performance_data-Full.csv"
data = pd.read_csv(file_path)

print("Dataset Overview:")
print(data.info())

if data.isnull().sum().sum() > 0:
    print("\nRemoving rows with missing values...")
    data = data.dropna()

roll_no = "102203644"
digit = int(roll_no[-1])

target_mapping = {
    0: "Target1", 5: "Target1",
    1: "Target2", 6: "Target2",
    2: "Target3", 7: "Target3",
    3: "Target4", 8: "Target4",
    4: "Target5", 9: "Target5"
}
target_col = target_mapping[digit]
print(f"\nChosen Target: {target_col}")

data = data[[target_col, *data.columns.difference([target_col])]]

X = data.drop(columns=[target_col])
y = data[target_col]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


def assess_model(model, X_train, X_test, y_train, y_test):
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"\nModel: {model.__class__.__name__}")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")
    return preds

linear_model = LinearRegression()
assess_model(linear_model, X_train, X_test, y_train, y_test)

decision_tree = DecisionTreeRegressor(random_state=42)
assess_model(decision_tree, X_train, X_test, y_train, y_test)

random_forest = RandomForestRegressor(random_state=42)
assess_model(random_forest, X_train, X_test, y_train, y_test)

evaluation_results = {
    "Model": ["Linear Regression", "Decision Tree", "Random Forest"],
    "MSE": [mean_squared_error(y_test, linear_model.predict(X_test)),
            mean_squared_error(y_test, decision_tree.predict(X_test)),
            mean_squared_error(y_test, random_forest.predict(X_test))],
    "R2 Score": [r2_score(y_test, linear_model.predict(X_test)),
                 r2_score(y_test, decision_tree.predict(X_test)),
                 r2_score(y_test, random_forest.predict(X_test))]
}
results_df = pd.DataFrame(evaluation_results)
print("\nSummary of Results:")
print(results_df)