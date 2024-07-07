import pandas as pd
from faker import Faker
import sqlite3

# Initialize Faker
fake = Faker()

# Generate customer data
customers = []
for _ in range(10):
    customers.append({
        "cust_id": fake.uuid4(),
        "name": fake.name(),
        "address": fake.address(),
        "street": fake.street_name(),
        "zip_code": fake.zipcode()
    })

customers_df = pd.DataFrame(customers)

# Generate branches data with reference to customer ids
branches = []
for _ in range(10):
    branches.append({
        "branch_id": fake.uuid4(),
        "location": fake.city(),
        "zip_code": fake.zipcode(),
        "cust_id": fake.random_element(elements=customers_df["cust_id"])
    })

branches_df = pd.DataFrame(branches)

# Function to create database and tables
def create_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create customer information table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        cust_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        street TEXT NOT NULL,
        zip_code TEXT NOT NULL
    )
    ''')
    
    # Create branches table if not exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS branches (
        branch_id TEXT PRIMARY KEY,
        location TEXT NOT NULL,
        zip_code TEXT NOT NULL,
        cust_id TEXT,
        FOREIGN KEY (cust_id) REFERENCES customers (cust_id)
    )
    ''')
    
    # Create additional tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS BATCH_JOB_INSTANCE  (
        JOB_INSTANCE_ID BIGINT  NOT NULL PRIMARY KEY,
        VERSION BIGINT,
        JOB_NAME VARCHAR(100) NOT NULL,
        JOB_KEY VARCHAR(32) NOT NULL,
        CONSTRAINT JOB_INST_UN UNIQUE (JOB_NAME, JOB_KEY)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS BATCH_JOB_EXECUTION  (
        JOB_EXECUTION_ID BIGINT  NOT NULL PRIMARY KEY,
        VERSION BIGINT,
        JOB_INSTANCE_ID BIGINT NOT NULL,
        CREATE_TIME TIMESTAMP NOT NULL,
        START_TIME TIMESTAMP DEFAULT NULL,
        END_TIME TIMESTAMP DEFAULT NULL,
        STATUS VARCHAR(10),
        EXIT_CODE VARCHAR(2500),
        EXIT_MESSAGE VARCHAR(2500),
        LAST_UPDATED TIMESTAMP,
        JOB_CONFIGURATION_LOCATION VARCHAR(2500) NULL,
        CONSTRAINT JOB_INST_EXEC_FK FOREIGN KEY (JOB_INSTANCE_ID)
        REFERENCES BATCH_JOB_INSTANCE(JOB_INSTANCE_ID)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS BATCH_JOB_EXECUTION_PARAMS  (
        JOB_EXECUTION_ID BIGINT NOT NULL,
        TYPE_CD VARCHAR(6) NOT NULL,
        KEY_NAME VARCHAR(100) NOT NULL,
        STRING_VAL VARCHAR(250),
        DATE_VAL TIMESTAMP DEFAULT NULL,
        LONG_VAL BIGINT,
        DOUBLE_VAL DOUBLE PRECISION,
        IDENTIFYING CHAR(1) NOT NULL,
        CONSTRAINT JOB_EXEC_PARAMS_FK FOREIGN KEY (JOB_EXECUTION_ID)
        REFERENCES BATCH_JOB_EXECUTION(JOB_EXECUTION_ID)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS BATCH_STEP_EXECUTION  (
        STEP_EXECUTION_ID BIGINT  NOT NULL PRIMARY KEY,
        VERSION BIGINT NOT NULL,
        STEP_NAME VARCHAR(100) NOT NULL,
        JOB_EXECUTION_ID BIGINT NOT NULL,
        START_TIME TIMESTAMP NOT NULL,
        END_TIME TIMESTAMP DEFAULT NULL,
        STATUS VARCHAR(10),
        COMMIT_COUNT BIGINT,
        READ_COUNT BIGINT,
        FILTER_COUNT BIGINT,
        WRITE_COUNT BIGINT,
        READ_SKIP_COUNT BIGINT,
        WRITE_SKIP_COUNT BIGINT,
        PROCESS_SKIP_COUNT BIGINT,
        ROLLBACK_COUNT BIGINT,
        EXIT_CODE VARCHAR(2500),
        EXIT_MESSAGE VARCHAR(2500),
        LAST_UPDATED TIMESTAMP,
        CONSTRAINT JOB_EXEC_STEP_FK FOREIGN KEY (JOB_EXECUTION_ID)
        REFERENCES BATCH_JOB_EXECUTION(JOB_EXECUTION_ID)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS BATCH_STEP_EXECUTION_CONTEXT  (
        STEP_EXECUTION_ID BIGINT NOT NULL PRIMARY KEY,
        SHORT_CONTEXT VARCHAR(2500),
        SERIALIZED_CONTEXT CLOB,
        CONSTRAINT STEP_EXEC_CTX_FK FOREIGN KEY (STEP_EXECUTION_ID)
        REFERENCES BATCH_STEP_EXECUTION(STEP_EXECUTION_ID)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS BATCH_JOB_EXECUTION_CONTEXT  (
        JOB_EXECUTION_ID BIGINT NOT NULL PRIMARY KEY,
        SHORT_CONTEXT VARCHAR(2500),
        SERIALIZED_CONTEXT CLOB,
        CONSTRAINT JOB_EXEC_CTX_FK FOREIGN KEY (JOB_EXECUTION_ID)
        REFERENCES BATCH_JOB_EXECUTION(JOB_EXECUTION_ID)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS BATCH_STEP_EXECUTION_SEQ  (
        ID BIGINT 
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS BATCH_JOB_EXECUTION_SEQ  (
        ID BIGINT 
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS BATCH_JOB_SEQ  (
        ID BIGINT 
    )
    ''')
    
    cursor.execute('''
    INSERT INTO BATCH_STEP_EXECUTION_SEQ (ID) VALUES (0)
    ''')
    
    cursor.execute('''
    INSERT INTO BATCH_JOB_EXECUTION_SEQ (ID) VALUES (0)
    ''')
    
    cursor.execute('''
    INSERT INTO BATCH_JOB_SEQ (ID) VALUES (0)
    ''')
    
    conn.commit()
    return conn

# Create both databases
test_db_conn = create_database('customer_branches_test.db')
prod_db_conn = create_database('customer_branches_prod.db')

# Function to insert data into the database
def insert_data(conn, customers_df, branches_df):
    cursor = conn.cursor()

    # Insert customer data
    for _, row in customers_df.iterrows():
        cursor.execute('''
        INSERT INTO customers (cust_id, name, address, street, zip_code)
        VALUES (?, ?, ?, ?, ?)
        ''', (row['cust_id'], row['name'], row['address'], row['street'], row['zip_code']))

    # Insert branches data
    for _, row in branches_df.iterrows():
        cursor.execute('''
        INSERT INTO branches (branch_id, location, zip_code, cust_id)
        VALUES (?, ?, ?, ?)
        ''', (row['branch_id'], row['location'], row['zip_code'], row['cust_id']))

    conn.commit()

# Insert data into both databases
insert_data(test_db_conn, customers_df, branches_df)
insert_data(prod_db_conn, customers_df, branches_df)

# Function to print database schema
def print_schema(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table_name in tables:
        table_name = table_name[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        print(f"Schema for table '{table_name}':")
        for column in columns:
            print(column)
        print()

# Print schema for both databases
print("Test Database Schema:")
print_schema(test_db_conn)

print("Production Database Schema:")
print_schema(prod_db_conn)

# Close the connections
test_db_conn.close()
prod_db_conn.close()
