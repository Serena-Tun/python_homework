import sqlite3
import pandas as pd
import os

# Task 5
# Path to your magazines database
DB_PATH = os.path.join("..", "db", "magazines.db")

# Connect to the database
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = 1")

# SQL query: join magazines and subscriptions
query = """
SELECT 
    m.id AS magazine_id,
    m.name AS magazine_name,
    COUNT(sub.id) AS num_subscribers
FROM magazines m
LEFT JOIN subscriptions sub ON m.id = sub.magazine_id
GROUP BY m.id, m.name;
"""

# Read into DataFrame
df = pd.read_sql_query(query, conn)

print("Magazine subscription summary:")
print(df.head())

# Add a dummy total column (example: total subscriptions * 1 for demo)
df['total'] = df['num_subscribers'] * 1
print("\nAfter adding 'total' column:")
print(df.head())

# Sort by magazine name
df = df.sort_values('magazine_name')

# Write to CSV in assignment8 folder
output_path = os.path.join(os.getcwd(), "order_summary.csv")
df.to_csv(output_path, index=False)
print(f"\nSummary written to {output_path}")

# Close connection
conn.close()
<<<<<<< HEAD

=======
>>>>>>> 548664d4d4c0e9273f1b8a413f9223d7641cfa28
print("Local version")
print("Remote version")
