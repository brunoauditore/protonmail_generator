import sqlite3


class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            return self.conn
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    def create_tables(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()

                # Create the "accounts" table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS accounts (
                        ID INTEGER PRIMARY KEY,
                        mail TEXT NOT NULL,
                        password TEXT NOT NULL,
                        Name TEXT,
                        Adress TEXT,
                        "mobile-phone" TEXT,
                        proxy TEXT,
                        "Card for Pay" TEXT
                    );
                ''')

                # Create the "orders" table with a foreign key reference to accounts
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY,
                        Name TEXT,
                        Link TEXT,
                        Store_name TEXT,
                        store_link TEXT,
                        price REAL,
                        date_creation TEXT,
                        id_account INTEGER,
                        FOREIGN KEY (id_account) REFERENCES accounts (ID)
                    );
                ''')

                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Error creating tables: {e}")

    def insert_account(self, data):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO accounts (mail, password, Name, Adress, "mobile-phone", proxy, "Card for Pay")
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', data)
                self.conn.commit()
                return cursor.lastrowid  # Get the ID of the newly inserted account
            except sqlite3.Error as e:
                print(f"Error inserting account: {e}")
        return None

    def insert_order(self, data):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                cursor.execute('''
                    INSERT INTO orders (Name, Link, Store_name, store_link, price, date_creation, id_account)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', data)
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"Error inserting order: {e}")

    def get_accounts_with_empty_mail(self):
        if self.conn:
            try:
                cursor = self.conn.cursor()
                query = "SELECT * FROM accounts WHERE mail = '' OR mail = '-';"
                cursor.execute(query)
                accounts = cursor.fetchall()
                return accounts
            except sqlite3.Error as e:
                print(f"Error retrieving accounts: {e}")
        return []

    def close(self):
        if self.conn:
            self.conn.close()


# Example usage:
if __name__ == "__main__":
    db_manager = DatabaseManager("my_database.db")
    connection = db_manager.connect()

    if connection:
        # Create tables
        db_manager.create_tables()

        # Insert account data and get the account ID
        account_data = (
        "user@example.com", "password123", "John Doe", "123 Main St", "555-123-4567", "proxy123", "credit-card")
        account_id = db_manager.insert_account(account_data)

        # Insert order data linked to the account ID
        order_data1 = (
        "Order 1", "https://example.com/order1", "Store 1", "https://example.com/store1", 100.0, "2023-09-26",
        account_id)
        order_data2 = (
        "Order 2", "https://example.com/order2", "Store 2", "https://example.com/store2", 150.0, "2023-09-27",
        account_id)

        db_manager.insert_order(order_data1)
        db_manager.insert_order(order_data2)

        # Close the database connection
        db_manager.close()