import sqlite3
from faker import Faker

# Initialize Faker instance
fake = Faker()

# Function to create the database structure (tables)
def create_tables(conn):
    cursor = conn.cursor()
    
    # Create the Customer table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            address TEXT
        );
    ''')

    # Create the Invoice table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoice (
            invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            invoice_date DATE NOT NULL,
            total_amount REAL NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
        );
    ''')

    # Create the Payments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER,
            payment_date DATE NOT NULL,
            amount_paid REAL NOT NULL,
            payment_method TEXT,
            FOREIGN KEY (invoice_id) REFERENCES invoice (invoice_id)
        );
    ''')

    conn.commit()

# Function to insert fake data into the test database
def insert_fake_data(conn, num_customers=10, num_invoices=5):
    cursor = conn.cursor()

    # Insert fake data into the customer table
    for _ in range(num_customers):
        name = fake.name()
        email = fake.email()
        phone = fake.phone_number()
        address = fake.address()
        
        cursor.execute('''
            INSERT INTO customer (name, email, phone, address)
            VALUES (?, ?, ?, ?)
        ''', (name, email, phone, address))
        
        customer_id = cursor.lastrowid  # Get the ID of the inserted customer
        
        # Insert fake invoices and payments for the customer
        for _ in range(num_invoices):
            invoice_date = fake.date_this_year()
            total_amount = round(fake.random_number(digits=4), 2)
            
            cursor.execute('''
                INSERT INTO invoice (customer_id, invoice_date, total_amount)
                VALUES (?, ?, ?)
            ''', (customer_id, invoice_date, total_amount))
            
            invoice_id = cursor.lastrowid  # Get the ID of the inserted invoice
            
            # Insert a payment for the invoice
            payment_date = fake.date_this_year()
            amount_paid = total_amount  # For simplicity, assume full payment
            payment_method = fake.credit_card_provider()
            
            cursor.execute('''
                INSERT INTO payments (invoice_id, payment_date, amount_paid, payment_method)
                VALUES (?, ?, ?, ?)
            ''', (invoice_id, payment_date, amount_paid, payment_method))

    conn.commit()

# Create two SQLite databases: one for test and one for QA
test_db = 'test.db'
qa_db = 'qa.db'

# Connect to both databases
conn_test = sqlite3.connect(test_db)
conn_qa = sqlite3.connect(qa_db)

# Create the tables in both databases
create_tables(conn_test)
create_tables(conn_qa)

# Insert fake data only into the test database
insert_fake_data(conn_test, num_customers=10, num_invoices=3)

# Close the connections
conn_test.close()
conn_qa.close()

print("Test and QA databases created. Data inserted into the test database.")
