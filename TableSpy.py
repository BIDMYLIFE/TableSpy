import pandas as pd
from sqlalchemy import create_engine

# 1. Connect to your MySQL database using the pymysql driver
# Format: mysql+pymysql://username:password@host:port/database
engine = create_engine('mysql+pymysql://pro_org:6B0##dd@rm-12345.mysql.rds.awscloud-ops.abc.com.us:3306/org_abc')

# 2. Load your table into a DataFrame
table_name = "staff_career"
df = pd.read_sql(f"SELECT * FROM {table_name}", engine)

# 3. Generate the report
print(f"=== DATA PROFILE REPORT FOR: {table_name.upper()} ===\n")

for column in df.columns:
    col_type = str(df[column].dtype)
    print(f"Column: {column} ({col_type})")
    print("-" * 40)
    
    # Check if the column is text/varchar-like
    if df[column].dtype == 'object' or isinstance(df[column].dtype, pd.CategoricalDtype):
        distinct_vals = df[column].dropna().unique()
        print(f"  Type Group: Text/Varchar")
        print(f"  Distinct Count: {len(distinct_vals)}")
        print(f"  Distinct Values Sample: {list(distinct_vals[:5])}") # Shows first 5
        
    # Check if the column is numeric
    elif pd.api.types.is_numeric_dtype(df[column]):
        print(f"  Type Group: Numeric")
        print(f"  Min: {df[column].min()}")
        print(f"  Avg: {df[column].mean():.2f}")
        print(f"  Max: {df[column].max()}")
        print(f"  Sample Count: {df[column].count()}")
        
    print("\n")