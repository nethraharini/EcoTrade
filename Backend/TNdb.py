import pandas as pd
from pymongo import MongoClient

# === Step 1: Connect to MongoDB ===
print("🔌 Connecting to MongoDB...")
client = MongoClient("mongodb://localhost:27017/")
db = client['waste_data']  # Database
collection = db['tn_collection']  # Collection

# === Step 2: Load CSV File ===
csv_path = "C:/Users/nethr/OneDrive/Desktop/ET/EcoTrade/Backend/TN.csv"
print(f"📂 Reading CSV from: {csv_path}")

try:
    df = pd.read_csv(csv_path)
    print("✅ CSV loaded successfully.")
    print("📋 First 5 rows:")
    print(df.head())
except Exception as e:
    print("❌ Error reading CSV:", e)
    exit()

# === Step 3: Convert DataFrame to Dictionary ===
data_dict = df.to_dict("records")
print(f"📦 Total records to insert: {len(data_dict)}")

# === Step 4: Clean Start (Optional) ===
collection.drop()
print("🧹 Old collection dropped for a fresh start.")

# === Step 5: Insert into MongoDB ===
if data_dict:
    collection.insert_many(data_dict)
    print("🎉 Data inserted into MongoDB successfully!")
else:
    print("⚠️ No data found to insert.")
