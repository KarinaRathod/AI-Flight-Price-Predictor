import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor

# Load dataset
df = pd.read_csv("Clean_Dataset.csv")

# Drop unnecessary column
df = df.drop(columns=["Unnamed: 0","flight"])

# Encode categorical columns
le_dict = {}

categorical_cols = [
    "airline",
    "source_city",
    "departure_time",
    "stops",
    "arrival_time",
    "destination_city",
    "class"
]

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    le_dict[col] = le

# Features and target
X = df.drop("price", axis=1)
y = df["price"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("flight_model.pkl", "wb"))

# Save encoders
pickle.dump(le_dict, open("encoders.pkl", "wb"))

print("Model Trained Successfully")