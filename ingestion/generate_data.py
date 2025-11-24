import duckdb
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import random

# Initialise Faker
fake = Faker()
Faker.seed(42)
random.seed(42)

# Connexion à DuckDB
db_path = "../data/analytics.duckdb"
conn = duckdb.connect(db_path)

print("🚀 Génération de données fictives...")

# 1. Génère des utilisateurs
users_data = []
for i in range(1, 101):  # 100 utilisateurs
    users_data.append({
        'user_id': i,
        'name': fake.name(),
        'email': fake.email(),
        'country': fake.country(),
        'created_at': fake.date_time_between(start_date='-2y', end_date='now')
    })

df_users = pd.DataFrame(users_data)
conn.execute("CREATE SCHEMA IF NOT EXISTS raw")
conn.execute("DROP TABLE IF EXISTS raw.users")
conn.execute("CREATE TABLE raw.users AS SELECT * FROM df_users")
print(f"✅ {len(df_users)} utilisateurs créés")

# 2. Génère des produits
products_data = []
categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports']
for i in range(1, 51):  # 50 produits
    products_data.append({
        'product_id': i,
        'product_name': fake.catch_phrase(),
        'category': random.choice(categories),
        'price': round(random.uniform(10, 500), 2)
    })

df_products = pd.DataFrame(products_data)
conn.execute("DROP TABLE IF EXISTS raw.products")
conn.execute("CREATE TABLE raw.products AS SELECT * FROM df_products")
print(f"✅ {len(df_products)} produits créés")

# 3. Génère des achats
purchases_data = []
for i in range(1, 501):  # 500 achats
    purchases_data.append({
        'purchase_id': i,
        'user_id': random.randint(1, 100),
        'product_id': random.randint(1, 50),
        'quantity': random.randint(1, 5),
        'purchase_date': fake.date_time_between(start_date='-1y', end_date='now')
    })

df_purchases = pd.DataFrame(purchases_data)
conn.execute("DROP TABLE IF EXISTS raw.purchases")
conn.execute("CREATE TABLE raw.purchases AS SELECT * FROM df_purchases")
print(f"✅ {len(df_purchases)} achats créés")

# Ferme la connexion
conn.close()

print("\n🎉 Données chargées avec succès dans DuckDB !")
print(f"📊 Base de données : {db_path}")