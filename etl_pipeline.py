from prefect import task, flow
import pandas as pd
from sqlalchemy import create_engine
from feature_engineering import process_text_features # Reusing your code!

# Define connection to your Docker Database
# Format: postgresql://user:password@localhost:port/database_name
DB_CONNECTION_URL = "postgresql://user:password@localhost:5432/pricing_data"

@task(name="Extract Data")
def extract_data(file_path):
    print(f"📥 Extracting data from {file_path}...")
    return pd.read_csv(file_path)

@task(name="Transform Data")
def transform_data(df):
    print("⚙️ Transforming data...")
    # 1. Clean the text features using your logic
    text_features = process_text_features(df['catalog_content'])
    
    # 2. Merge them back
    df_clean = pd.concat([df, text_features], axis=1)
    
    # 3. Handle missing values (Basic DE task)
    df_clean.fillna(0, inplace=True)
    
    print(f"   Data shape after cleanup: {df_clean.shape}")
    return df_clean

@task(name="Load to DB")
def load_data(df, table_name):
    print(f"💾 Loading data into table: '{table_name}'...")
    engine = create_engine(DB_CONNECTION_URL)
    
    # This one line does all the SQL magic
    # if_exists='replace' means it overwrites old data (good for dev)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print("✅ Data successfully saved to Postgres!")

@flow(name="Pricing Data Pipeline")
def main_pipeline():
    # The workflow logic
    raw_data = extract_data("train.csv")
    clean_data = transform_data(raw_data)
    load_data(clean_data, "products_cleaned")

if __name__ == "__main__":
    main_pipeline()