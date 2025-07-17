# sweet_shop_manager.py

"""
Sweet Shop Management System
A TDD-based implementation for managing a sweet shop inventory
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import os


class SweetCategory(Enum):
    NUT_BASED = "Nut-Based"
    MILK_BASED = "Milk-Based"
    VEGETABLE_BASED = "Vegetable-Based"
    CHOCOLATE = "Chocolate"
    CANDY = "Candy"
    PASTRY = "Pastry"
    UNCATEGORIZED = "Uncategorized"


@dataclass
class Sweet:
    id: int
    name: str
    category: SweetCategory
    price: float
    quantity: int

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if not self.name.strip():
            raise ValueError("Name cannot be empty")

    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.value,
            'price': self.price,
            'quantity': self.quantity
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Sweet':
        return cls(
            id=data['id'],
            name=data['name'],
            category=SweetCategory(data.get('category', 'Uncategorized')),
            price=data['price'],
            quantity=data['quantity']
        )


class SweetShopManager:
    def __init__(self, filename='sweet_shop_data.json'):
        self.filename = filename
        self._sweets: Dict[int, Sweet] = {}
        self._next_id = 1001
        self.load_from_file()

    def load_from_file(self):
        if not os.path.exists(self.filename):
            self.save_to_file()  # Create file with empty structure

        with open(self.filename, 'r') as f:
            data = json.load(f)

        self._sweets = {s['id']: Sweet.from_dict(s) for s in data.get('sweets', [])}
        self._next_id = data.get('next_id', 1001)

    def save_to_file(self):
        data = {
            'sweets': [s.to_dict() for s in self._sweets.values()],
            'next_id': self._next_id
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def get_all_items(self) -> List[Sweet]:
        return list(self._sweets.values())

    def add_item(self, name: str, quantity: int, price: float, category: str = "Uncategorized") -> Sweet:
        new_id = self._next_id
        self._next_id += 1
        sweet = Sweet(new_id, name, SweetCategory(category), price, quantity)
        self._sweets[new_id] = sweet
        self.save_to_file()
        return sweet

    def delete_item(self, sweet_id: int):
        if sweet_id in self._sweets:
            del self._sweets[sweet_id]
            self.save_to_file()

    def update_item(self, sweet_id: int, name: str, quantity: int, price: float):
        if sweet_id in self._sweets:
            sweet = self._sweets[sweet_id]
            sweet.name = name
            sweet.quantity = quantity
            sweet.price = price
            self.save_to_file()

    def search_by_name(self, name: str) -> List[Sweet]:
        return [s for s in self._sweets.values() if name.lower() in s.name.lower()]

    def search_by_category(self, category: str) -> List[Sweet]:
        return [s for s in self._sweets.values() if s.category.value == category]

    def search_by_price_range(self, min_price: float, max_price: float) -> List[Sweet]:
        return [s for s in self._sweets.values() if min_price <= s.price <= max_price]

    def sort_sweets_by_name(self) -> List[Sweet]:
        return sorted(self._sweets.values(), key=lambda s: s.name.lower())

    def sort_sweets_by_price(self, reverse=False) -> List[Sweet]:
        return sorted(self._sweets.values(), key=lambda s: s.price, reverse=reverse)

    def sort_sweets_by_quantity(self, reverse=False) -> List[Sweet]:
        return sorted(self._sweets.values(), key=lambda s: s.quantity, reverse=reverse)

    def clear_inventory(self):
        self._sweets.clear()
        self._next_id = 1001
        self.save_to_file()
        import json

DATA_FILE = 'data.json'

# Load data from JSON file
def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Get all items
def get_all_items():
    data = load_data()
    return data['sweets']

# Add a new item
def add_item(name, quantity, price, category):
    data = load_data()
    new_id = data['next_id'] + 1
    new_sweet = {
        "id": new_id,
        "name": name,
        "category": category,
        "price": price,
        "quantity": quantity
    }
    data['sweets'].append(new_sweet)
    data['next_id'] = new_id
    save_data(data)

# Delete item by ID
def delete_item(sweet_id):
    data = load_data()
    data['sweets'] = [item for item in data['sweets'] if item['id'] != sweet_id]
    save_data(data)

# Update item by ID
def update_item(sweet_id, name, quantity, price, category):
    data = load_data()
    for item in data['sweets']:
        if item['id'] == sweet_id:
            item['name'] = name
            item['quantity'] = quantity
            item['price'] = price
            item['category'] = category
            break
    save_data(data)

