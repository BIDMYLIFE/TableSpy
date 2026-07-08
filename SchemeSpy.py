import pandas as pd
from sqlalchemy import create_engine, text

# 1. Connect to MySQL
# Change 'your_schema_name' to your actual database/schema name
schema_name = "org_abc" 
engine = create_engine('mysql+pymysql://pro_org:6B0##dd@rm-12345.mysql.rds.awscloud-ops.abc.com.us:3306/org_abc')

# 2. Fetch all table names in this schema
table_query = text("""
    SELECT TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_SCHEMA = :schema AND TABLE_TYPE = 'BASE TABLE'
""")

with engine.connect() as connection:
    tables = [row[0] for row in connection.execute(table_query, {"schema": schema_name})]

# 3. Loop through every table and profile it
for table_name in tables:
    print(f"\n==================================================")
    print(f"=== DATA PROFILE REPORT FOR: {table_name.upper()} ===")
    print(f"==================================================")
    
    # Read the individual table
    df = pd.read_sql(f"SELECT * FROM `{table_name}`", engine)
    
    if df.empty:
        print("  (Table is empty)")
        continue

    for column in df.columns:
        col_type = str(df[column].dtype)
        print(f"Column: {column} ({col_type})")
        print("-" * 40)
        
        # Check text/varchar
        if df[column].dtype == 'object' or isinstance(df[column].dtype, pd.CategoricalDtype):
            distinct_vals = df[column].dropna().unique()
            print(f"  Type Group: Text/Varchar")
            print(f"  Distinct Count: {len(distinct_vals)}")
            print(f"  Distinct Values Sample: {list(distinct_vals[:5])}")
            
        # Check numeric
        elif pd.api.types.is_numeric_dtype(df[column]):
            print(f"  Type Group: Numeric")
            print(f"  Min: {df[column].min()}")
            print(f"  Avg: {df[column].mean():.2f}")
            print(f"  Max: {df[column].max()}")