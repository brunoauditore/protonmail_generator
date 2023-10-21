import json

# Define a function to read the proxy URLs from the JSON file
from db import DatabaseManager


def read_proxy_urls_from_json(filename):
    try:
        with open(filename, "r") as file:
            proxy_urls = json.load(file)
            return proxy_urls
    except FileNotFoundError:
        print(f"The file '{filename}' does not exist.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data in '{filename}': {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return []

def put_proxy_to_table(db,list):
    for el in list:
        account_data = (
            "-", "-", "-", "-", "-", el, "-")
        db.insert_account(account_data)
        print(account_data)

list = read_proxy_urls_from_json("proxy.json")
db = DatabaseManager("my_database.db")
db.connect()

# put_proxy_to_table(db,list)

print(db.get_accounts_with_empty_mail())



db.close()