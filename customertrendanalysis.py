# Preprocessing the csv data and loading it into a postgres sql database

import pandas as pd
import numpy as np

df = pd.read_csv('customer_shopping_behavior.csv')
df.head()

df.info()

df.describe(include='all')

df.isnull().sum()

df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))

df.isnull().sum()

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')
df = df.rename(columns={'purchase_amount_(usd)' : 'purchase_amount'})
df.columns

labels = ['Young Adult', 'Adult', 'Middle Aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)
df.head()

frequency_mapping = {
    'Fortnightly': 14,
    'Weekly' : 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 months': 90
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
df[['frequency_of_purchases', 'purchase_frequency_days']].head(10)

df.isnull().sum()

df[['discount_applied', 'promo_code_used']].head()

(df['discount_applied'] == df['promo_code_used']).all()

df.drop('promo_code_used', axis=1)
df.head()

pip install psycopg2-binary sqlalchemy

from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("databaseUrl")
engine = create_engine(DATABASE_URL)
conn = engine.connect()
print("Connected successfully")

table_name = "customer"
df.to_sql(table_name, engine, if_exists = "replace", index = False)
print(f"Data successfully loaded into the table '{table_name}'. ")
