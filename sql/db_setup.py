import sqlite3
import os

# setting up simple file paths
db_dir = "data/db"
db_path = "data/db/bluestock_mf.db"
schema_path = "sql/schema.sql"

print("Starting to build database tables...")

# make sure the folder for the database exists first
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

# open and read our schema.sql file step by step
with open(schema_path, 'r') as f:
    sql_script = f.read()

# connect to the sqlite database file
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # run all the sql queries inside schema.sql to make the tables
    cursor.executescript(sql_script)
    conn.commit()
    print("Success: database has been initialized with all 7 tables!")
except Exception as e:
    # print an error if something goes wrong
    print("Error running the sql script:", str(e))
finally:
    # always close the connection when done
    conn.close()

print("Database setup finished!")