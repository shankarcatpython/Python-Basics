import sqlite3
import json

# Function to get the next available ID from a table
def get_next_id(conn, table_name, id_column):
    cursor = conn.cursor()
    cursor.execute(f'SELECT MAX({id_column}) FROM {table_name}')
    max_id = cursor.fetchone()[0]
    return (max_id or 0) + 1

# Function to insert customers, invoices, and payments into the QA database and track stats
def insert_data_into_qa(conn, data):
    cursor = conn.cursor()

    # Initialize stats dictionary
    stats = {
        'customers': 0,
        'invoices': 0,
        'payments': 0
    }

    # Loop through each customer in the JSON data
    for customer in data:
        # Get the next available customer_id
        next_customer_id = get_next_id(conn, 'customer', 'customer_id')

        # Insert the customer data
        cursor.execute('''
            INSERT INTO customer (customer_id, name, email, phone, address)
            VALUES (?, ?, ?, ?, ?)
        ''', (next_customer_id, customer['name'], customer['email'], customer['phone'], customer['address']))

        # Update stats for customers
        stats['customers'] += 1

        # If the customer has invoices, insert them
        if 'invoices' in customer:
            for invoice in customer['invoices']:
                # Get the next available invoice_id
                next_invoice_id = get_next_id(conn, 'invoice', 'invoice_id')

                # Insert the invoice data
                cursor.execute('''
                    INSERT INTO invoice (invoice_id, customer_id, invoice_date, total_amount)
                    VALUES (?, ?, ?, ?)
                ''', (next_invoice_id, next_customer_id, invoice['invoice_date'], invoice['total_amount']))

                # Update stats for invoices
                stats['invoices'] += 1

                # If the invoice has payments, insert them
                if 'payments' in invoice:
                    for payment in invoice['payments']:
                        # Get the next available payment_id
                        next_payment_id = get_next_id(conn, 'payments', 'payment_id')

                        # Insert the payment data
                        cursor.execute('''
                            INSERT INTO payments (payment_id, invoice_id, payment_date, amount_paid, payment_method)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (next_payment_id, next_invoice_id, payment['payment_date'], payment['amount_paid'], payment['payment_method']))

                        # Update stats for payments
                        stats['payments'] += 1

    # Commit the changes
    conn.commit()

    return stats

# Load data from the JSON file
with open('all_customers_data.json', 'r') as json_file:
    customer_data = json.load(json_file)

# Connect to the QA database
conn_qa = sqlite3.connect('qa.db')

# Insert the data into the QA database and get stats
stats = insert_data_into_qa(conn_qa, customer_data)

# Close the connection
conn_qa.close()

# Write the stats to a JSON file
with open('stats.json', 'w') as stats_file:
    json.dump(stats, stats_file, indent=4)

print(f"Data inserted into QA database successfully. Stats written to stats.json.")
