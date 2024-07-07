import sqlite3
import json

# Function to fetch data for a given customer from the database
def fetch_customer_data(conn, cust_id):
    cursor = conn.cursor()
    
    # Fetch customer data
    cursor.execute("SELECT * FROM customers WHERE cust_id = ?", (cust_id,))
    customer_data = cursor.fetchone()
    customer_columns = [description[0] for description in cursor.description]
    
    # Fetch branch data for the customer
    cursor.execute("SELECT * FROM branches WHERE cust_id = ?", (cust_id,))
    branch_data = cursor.fetchall()
    branch_columns = [description[0] for description in cursor.description]
    
    return customer_data, customer_columns, branch_data, branch_columns

# Function to create the database and tables if they don't exist
def create_test_database(db_name):
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

    conn.commit()
    return conn

# Function to insert data into the test database
def insert_data_from_json(conn, data):
    cursor = conn.cursor()

    # Insert customer and branch data
    for customer in data:
        # Insert customer data
        cursor.execute('''
        INSERT INTO customers (cust_id, name, address, street, zip_code)
        VALUES (?, ?, ?, ?, ?)
        ''', (customer['cust_id'], customer['name'], customer['address'], customer['street'], customer['zip_code']))

        # Insert branch data for this customer
        for branch in customer['branches']:
            cursor.execute('''
            INSERT INTO branches (branch_id, location, zip_code, cust_id)
            VALUES (?, ?, ?, ?)
            ''', (branch['branch_id'], branch['location'], branch['zip_code'], branch['cust_id']))

    conn.commit()

# Extract data from production database and write to JSON
def extract_data_to_json(prod_db_conn, json_file_name):
    # Fetch all customer IDs
    cursor = prod_db_conn.cursor()
    cursor.execute("SELECT cust_id FROM customers")
    customer_ids = cursor.fetchall()

    # Initialize list to hold all customer data
    all_customers_data = []

    for cust_id in customer_ids:
        cust_id = cust_id[0]  # Extract cust_id from tuple
        customer_data, customer_columns, branch_data, branch_columns = fetch_customer_data(prod_db_conn, cust_id)
        
        # Create a dictionary for the customer data
        customer_dict = dict(zip(customer_columns, customer_data))
        
        # Create a list of dictionaries for the branch data
        branches_list = [dict(zip(branch_columns, branch)) for branch in branch_data]
        
        # Combine customer data and branch data
        customer_dict["branches"] = branches_list
        
        # Add the combined data to the list of all customers
        all_customers_data.append(customer_dict)

    # Write the data to a JSON file
    with open(json_file_name, 'w') as file:
        json.dump(all_customers_data, file, indent=4)

# Main execution flow
def main():
    # Step 1: Extract data from production database
    prod_db_conn = sqlite3.connect('customer_branches_prod.db')
    extract_data_to_json(prod_db_conn, 'customer_records.json')
    prod_db_conn.close()
    print("Data has been extracted from customer_branches_prod.db to customer_records.json")

    # Step 2: Insert data into the test database
    with open('customer_records.json', 'r') as file:
        data = json.load(file)

    test_db_conn = create_test_database('final_test.db')
    insert_data_from_json(test_db_conn, data)
    test_db_conn.close()
    print("Data has been inserted into final_test.db")

if __name__ == '__main__':
    main()
