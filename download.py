import sqlite3
import json
import os

# Function to dynamically fetch data from any table
def fetch_table_data(conn, table_name):
    cursor = conn.cursor()

    # Query to fetch all rows and column names dynamically from the table
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()

    # Get the column names for the table
    column_names = [description[0] for description in cursor.description]

    # Create a list of dictionaries representing each row as a JSON object
    table_data = [dict(zip(column_names, row)) for row in rows]

    return table_data

# Function to fetch related data dynamically for customer, invoice, and payments
def fetch_customer_data_dynamically(conn):
    # Fetch customer data
    customers = fetch_table_data(conn, 'customer')

    for customer in customers:
        customer_id = customer.get('customer_id')

        # Fetch related invoices dynamically for each customer
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM invoice WHERE customer_id = ?', (customer_id,))
        invoices = cursor.fetchall()

        if invoices:
            column_names = [description[0] for description in cursor.description]
            customer['invoices'] = [dict(zip(column_names, invoice)) for invoice in invoices]

            # For each invoice, fetch related payments dynamically
            for invoice in customer['invoices']:
                invoice_id = invoice.get('invoice_id')

                cursor.execute(f'SELECT * FROM payments WHERE invoice_id = ?', (invoice_id,))
                payments = cursor.fetchall()

                if payments:
                    column_names = [description[0] for description in cursor.description]
                    invoice['payments'] = [dict(zip(column_names, payment)) for payment in payments]

    return customers

# Connect to the test database
conn_test = sqlite3.connect('test.db')

# Fetch customer data dynamically
customer_data = fetch_customer_data_dynamically(conn_test)

# Close the connection
conn_test.close()

# Write the data to a single JSON file
output_file = 'all_customers_data.json'
with open(output_file, 'w') as json_file:
    json.dump(customer_data, json_file, indent=4)

print(f"All customer data written to {output_file}")
