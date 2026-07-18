import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# Settings
NUM_ROWS = 5000
regions = ["North America", "Europe", "Asia Pacific", "Latin America"]
products = ["Laptop", "Monitor", "Keyboard", "Mouse", "Headphones", "Webcam"]

# Generate fake rows
rows = []
start_date = datetime(2024, 1, 1)

for i in range(NUM_ROWS):
    transaction_id = i + 1
    transaction_date = start_date + timedelta(days=random.randint(0, 500))
    region = random.choice(regions)
    product = random.choice(products)
    quantity = random.randint(1, 10)
    unit_price = round(random.uniform(20, 500), 2)
    revenue = round(quantity * unit_price, 2)
    cost = round(revenue * random.uniform(0.5, 0.8), 2)  # cost is 50-80% of revenue

    rows.append({
        "transaction_id": transaction_id,
        "transaction_date": transaction_date.strftime("%Y-%m-%d"),
        "region": region,
        "product": product,
        "quantity": quantity,
        "unit_price": unit_price,
        "revenue": revenue,
        "cost": cost
    })

# Inject an anomaly: Europe's Q2 2025 costs spike (simulating a shipping crisis)
anomaly_rows = []
for i in range(300):
    transaction_id = NUM_ROWS + i + 1
    transaction_date = datetime(2025, 5, random.randint(1, 28))
    quantity = random.randint(1, 10)
    unit_price = round(random.uniform(20, 500), 2)
    revenue = round(quantity * unit_price, 2)
    cost = round(revenue * random.uniform(0.75, 0.95), 2)  # much higher cost ratio!

    anomaly_rows.append({
        "transaction_id": transaction_id,
        "transaction_date": transaction_date.strftime("%Y-%m-%d"),
        "region": "Europe",
        "product": "Monitor",
        "quantity": quantity,
        "unit_price": unit_price,
        "revenue": revenue,
        "cost": cost
    })

rows.extend(anomaly_rows)

# Create DataFrame and save to CSV
df = pd.DataFrame(rows)
df.to_csv("sales_data.csv", index=False)

print(f"✅ Generated {NUM_ROWS} fake sales rows into sales_data.csv")