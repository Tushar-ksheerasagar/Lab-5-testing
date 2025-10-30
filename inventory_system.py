"""Inventory management system with logging and JSON persistence."""

import json
import logging
from datetime import datetime

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Global constant for default inventory file
INVENTORY_FILE = "inventory.json"

# Global variable for stock data
STOCK_DATA = {}


def add_item(item="default", qty=0, logs=None):
    """Add a quantity of an item to the stock.

    Args:
        item (str): Item name to add.
        qty (int): Quantity to add.
        logs (list, optional): Log list to record actions.
    """
    if logs is None:
        logs = []

    if not isinstance(item, str) or not isinstance(qty, int):
        logging.error("Invalid item or quantity type for item '%s'", item)
        return

    STOCK_DATA[item] = STOCK_DATA.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info("Added %d of %s", qty, item)


def remove_item(item, qty):
    """Remove quantity of an item from stock.

    Args:
        item (str): Item name to remove.
        qty (int): Quantity to remove.
    """
    if not isinstance(item, str) or not isinstance(qty, int):
        logging.error("Invalid item or quantity type for removal.")
        return

    try:
        if item not in STOCK_DATA:
            raise KeyError(f"Item '{item}' not found")
        STOCK_DATA[item] -= qty
        if STOCK_DATA[item] <= 0:
            del STOCK_DATA[item]
        logging.info("Removed %d of %s", qty, item)
    except KeyError as exc:
        logging.warning(exc)


def get_qty(item):
    """Get current quantity of an item.

    Args:
        item (str): Item name to query.

    Returns:
        int: Quantity available, 0 if not found.
    """
    return STOCK_DATA.get(item, 0)


def load_data(file_path=INVENTORY_FILE):
    """Load stock data from JSON file.

    Args:
        file_path (str): Path to file to load from.
    """
    global STOCK_DATA
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            STOCK_DATA = json.load(file)
        logging.info("Loaded inventory from %s", file_path)
    except FileNotFoundError:
        logging.warning("Inventory file not found, starting with empty data.")
        STOCK_DATA = {}


def save_data(file_path=INVENTORY_FILE):
    """Save stock data to JSON file.

    Args:
        file_path (str): Path to file to save to.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(STOCK_DATA, file, indent=4)
        logging.info("Saved inventory to %s", file_path)
    except (IOError, TypeError) as exc:
        logging.error("Failed to save inventory: %s", exc)


def print_data():
    """Print item stock report to console."""
    print("Items Report:")
    for item, qty in STOCK_DATA.items():
        print(f"{item} -> {qty}")


def check_low_items(threshold=5):
    """Return list of items with quantity below threshold.

    Args:
        threshold (int): Threshold below which items are considered low.

    Returns:
        list: List of item names with low stock.
    """
    return [item for item, qty in STOCK_DATA.items() if qty < threshold]


def main():
    """Main function to demonstrate inventory operations."""
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")  # Invalid types handled
    remove_item("apple", 3)
    remove_item("orange", 1)

    print(f"Apple stock: {get_qty('apple')}")
    print(f"Low items: {check_low_items()}")
    save_data()
    load_data()
    print_data()


if __name__ == "__main__":
    main()
