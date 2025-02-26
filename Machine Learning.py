from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

# Load data (replace with actual file path)
df = pd.read_csv("your_combined_data.csv")

# Encode categorical variables (e.g., team names, prop types)
label_encoder = LabelEncoder()
df["Prop Type"] = label_encoder.fit_transform(df["Prop Type"])
df["Team"] = label_encoder.fit_transform(df["Team"])
df["Opponent"] = label_encoder.fit_transform(df["Opponent"])

# Define features (X) and target (y)
features = ["PPG", "RPG", "APG", "Prop Type", "Prop Value", "Opponent Defense", "Injury Impact"]
X = df[features]
y = df["Actual Result"].map({"Over": 1, "Under": 0})  # Convert "Over/Under" to binary labels

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale numeric features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate performance
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
print(classification_report(y_test, y_pred))


def predict_prop(player, stats):
    """
    Predict Over/Under for a given player.
    stats = {"PPG": 25, "RPG": 5, "APG": 6, "Prop Value": 24.5, "Opponent Defense": 7, "Injury Impact": 0}
    """
    input_data = scaler.transform([[stats["PPG"], stats["RPG"], stats["APG"], stats["Prop Value"], stats["Opponent Defense"], stats["Injury Impact"]]])
    prediction = model.predict(input_data)[0]
    return "Over" if prediction == 1 else "Under"

# Example Usage
player_stats = {"PPG": 25, "RPG": 5, "APG": 6, "Prop Value": 24.5, "Opponent Defense": 7, "Injury Impact": 0}
print(predict_prop("LeBron James", player_stats))
