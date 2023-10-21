import json

# Define a function to read the proxy URLs from the JSON file
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

# Read proxy URLs from the "proxy.json" file
proxy_urls = read_proxy_urls_from_json("proxy.json")

# Extract and print proxy information from each URL
