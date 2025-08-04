# Import Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

#read the dataset
df = pd.read_csv("/content/drive/MyDrive/dataset/UCI_Credit_Card.csv.zip")
print("First 5 rows:")
print(df.head())
print("\nDataset Info:")
print(df.info())

#Handle Missing Data
print("\nMissing Values:")
print(df.isnull().sum())

for col in df.select_dtypes(include=['float64', 'int64']):
    df[col].fillna(df[col].median(), inplace=True)
for col in df.select_dtypes(include=['object']):
    df[col].fillna(df[col].mode()[0], inplace=True)

le = LabelEncoder()
for col in df.select_dtypes(include=['object']):
    df[col] = le.fit_transform(df[col])

X = df.iloc[:, :-1]   
y = df.iloc[:, -1]    

# 6. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 8. Logistic Regression Model
log_model = LogisticRegression(max_iter=500)
log_model.fit(X_train, y_train)

y_pred_log = log_model.predict(X_test)

print("Logistic Regression Results")
print("Accuracy", accuracy_score(y_test, y_pred_log))
print("Confusion Matrix", confusion_matrix(y_test, y_pred_log))
print("Classification Report", classification_report(y_test, y_pred_log))

# 9. Random Forest Model
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

y_pred_rf = rf_model.predict(X_test)

print("Random Forest Results")
print("Accuracy", accuracy_score(y_test, y_pred_rf))
print("Confusion Matrix", confusion_matrix(y_test, y_pred_rf))
print("Classification Report", classification_report(y_test,y_pred_rf))