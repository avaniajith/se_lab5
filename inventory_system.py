"""
A simple inventory management system module.

This module provides functions to add, remove, and query items
in an inventory, which is stored in a JSON file.
"""

import json
import logging

# We no longer use a global variable.
# The stock data will be managed in main and passed to functions.


def add_item(stock: dict, item: str, qty: int):
    """
    Adds a specified quantity of an item to the stock.

    Args:
        stock (dict): The inventory dictionary to modify.
        item (str): The name of the item.
        qty (int): The quantity to add.
    """
    # Input Validation
    if not isinstance(item, str) or not item:
        logging.error("Invalid item name: %s. Item must be a non-empty string.", item)
        return
    if not isinstance(qty, int):
        logging.error("Invalid quantity: %s. Quantity must be an integer.", qty)
        return

    stock[item] = stock.get(item, 0) + qty
    logging.info("Added %d of %s. New total: %d", qty, item, stock[item])


def remove_item(stock: dict, item: str, qty: int):
    """
    Removes a specified quantity of an item from the stock.

    If the quantity falls to 0 or below, the item is removed.

    Args:
        stock (dict): The inventory dictionary to modify.
        item (str): The name of the item.
        qty (int): The quantity to remove.
    """
    # Input Validation
    if not isinstance(item, str) or not item:
        logging.error("Invalid item name: %s. Item must be a non-empty string.", item)
        return
    if not isinstance(qty, int):
        logging.error("Invalid quantity: %s. Quantity must be an integer.", qty)
        return

    try:
        stock[item] -= qty
        if stock[item] <= 0:
            del stock[item]
            logging.info("Removed %d of %s. Item removed from stock.", qty, item)
        else:
            logging.info("Removed %d of %s. New total: %d", qty, item, stock[item])
    except KeyError:
        # Replaced bare 'except' with specific 'KeyError'
        logging.warning("Attempted to remove '%s', but it is not in stock.", item)


def get_qty(stock: dict, item: str) -> int:
    """
    Gets the current quantity of a specific item.

    Args:
        stock (dict): The inventory dictionary.
        item (str): The name of the item to query.

    Returns:
        int: The quantity of the item, or 0 if not found.
    """
    # Use .get() to prevent KeyError for items not in stock
    return stock.get(item, 0)


def load_data(file: str = "inventory.json") -> dict:
    """
    Loads inventory data from a JSON file.

    Args:
        file (str, optional): The name of the file to load from.

    Returns:
        dict: The loaded inventory data, or an empty dict if file not found
              or data is invalid.
    """
    try:
        # Use 'with' and specify 'encoding'
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
            if not isinstance(stock_data, dict):
                logging.error("Invalid data format in %s. Starting new inventory.", file)
                return {}
            return stock_data
    except FileNotFoundError:
        logging.warning("%s not found. Starting with an empty inventory.", file)
        return {}
    except json.JSONDecodeError:
        logging.error("Error decoding JSON from %s. Starting new inventory.", file)
        return {}


def save_data(stock: dict, file: str = "inventory.json"):
    """
    Saves the current inventory data to a JSON file.

    Args:
        stock (dict): The inventory dictionary to save.
        file (str, optional): The name of the file to save to.
    """
    try:
        # Use 'with' and specify 'encoding'
        with open(file, "w", encoding="utf-8") as f:
            json.dump(stock, f, indent=4)
            logging.info("Inventory successfully saved to %s", file)
    except IOError as e:
        logging.error("Could not write to file %s: %s", file, e)


def print_data(stock: dict):
    """
    Prints a formatted report of all items in stock.

    Args:
        stock (dict): The inventory dictionary to print.
    """
    print("\n--- Items Report ---")
    if not stock:
        print("Inventory is empty.")
    else:
        for item, qty in stock.items():
            print(f"{item} -> {qty}")
    print("--------------------\n")


def check_low_items(stock: dict, threshold: int = 5) -> list:
    """
    Finds items with a quantity below the specified threshold.

    Args:
        stock (dict): The inventory dictionary.
        threshold (int, optional): The low-stock threshold.

    Returns:
        list: A list of item names that are low in stock.
    """
    result = []
    for item, qty in stock.items():
        if qty < threshold:
            result.append(item)
    return result


def main():
    """
    Main function to run the inventory system operations.
    """
    # Configure logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # No global variable. Load data into a local variable.
    stock_data = load_data()

    # Pass 'stock_data' to all functions
    add_item(stock_data, "apple", 10)
    add_item(stock_data, "banana", -2)  # Will log a negative addition
    add_item(stock_data, 123, "ten")    # Will be caught by input validation
    remove_item(stock_data, "apple", 3)
    remove_item(stock_data, "orange", 1)  # Will be caught by KeyError handler

    print(f"Apple stock: {get_qty(stock_data, 'apple')}")
    print(f"Low items: {check_low_items(stock_data)}")

    save_data(stock_data)
    load_data()  # Load again to check persistence
    print_data(stock_data)

    # 'eval' has been removed.


# Standard Python practice to run main()
if __name__ == "__main__":
    main()