#!/usr/bin/env python3
"""Sweet Shop Management System - CLI"""

from sweet_shop_manager import (
    SweetShopManager, SweetCategory,
    InsufficientStockError, SweetNotFoundError
)

class SweetShopCLI:
    def __init__(self):
        self.shop = SweetShopManager()
        self.data_file = "sweet_shop_data.json"
        self.load_data()
        if not self.shop.view_all_sweets():
            self.load_sample_data()

    def load_data(self):
        try:
            self.shop.load_from_file(self.data_file)
            print(f"Loaded data from {self.data_file}")
        except:
            print("No existing data found. Starting fresh.")

    def save_data(self):
        try:
            self.shop.save_to_file(self.data_file)
            print(f"Data saved to {self.data_file}")
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_sample_data(self):
        print("Loading sample data...")
        samples = [
            ("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20),
            ("Gulab Jamun", SweetCategory.MILK_BASED, 10.0, 50),
            ("Gajar Halwa", SweetCategory.VEGETABLE_BASED, 30.0, 15),
            ("Dark Chocolate", SweetCategory.CHOCOLATE, 80.0, 25),
            ("Rasgulla", SweetCategory.MILK_BASED, 12.0, 40),
            ("Badam Burfi", SweetCategory.NUT_BASED, 60.0, 18),
            ("Chocolate Cake", SweetCategory.PASTRY, 120.0, 8),
            ("Jalebi", SweetCategory.CANDY, 15.0, 35)
        ]
        for name, cat, price, qty in samples:
            self.shop.add_sweet(name, cat, price, qty)
        print("Sample data loaded.")

    def display_menu(self):
        print("\n" + "="*40)
        print(" Sweet Shop Management System")
        print("="*40)
        print("1. Add Sweet    2. Delete Sweet")
        print("3. View All     4. Search Sweets")
        print("5. Purchase     6. Restock")
        print("7. Update Price 8. Sort Sweets")
        print("9. Reports      10. Save & Exit")
        print("0. Exit without saving")

    def display_table(self, sweets, title="Inventory"):
        if not sweets:
            print(f"\n{title}: No items.")
            return
        print(f"\n{title}:")
        print("-" * 70)
        print(f"{'ID':<5}{'Name':<20}{'Category':<15}{'Price':<10}{'Stock':<10}")
        print("-" * 70)
        for s in sweets:
            print(f"{s.id:<5}{s.name:<20}{s.category.value:<15}₹{s.price:<9.2f}{s.quantity:<10}")
        print("-" * 70)

    def get_category(self):
        print("\nSelect Category:")
        for i, cat in enumerate(SweetCategory, 1):
            print(f"{i}. {cat.value}")
        try:
            idx = int(input("Choice: "))
            return list(SweetCategory)[idx - 1]
        except:
            print("Invalid category.")
            return None

    def add_sweet(self):
        print("\n--- Add Sweet ---")
        name = input("Sweet name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        category = self.get_category()
        if not category:
            return
        try:
            price = float(input("Price: ₹"))
            quantity = int(input("Quantity: "))
            self.shop.add_sweet(name, category, price, quantity)
            print("Sweet added.")
        except Exception as e:
            print(f"Error: {e}")

    def delete_sweet(self):
        try:
            sid = int(input("Enter sweet ID to delete: "))
            sweet = self.shop.get_sweet(sid)
            confirm = input(f"Delete {sweet.name}? (y/N): ").lower()
            if confirm == 'y':
                self.shop.delete_sweet(sid)
                print("Deleted.")
        except Exception as e:
            print(f"Error: {e}")

    def search_sweets(self):
        print("\nSearch by: 1. Name  2. Category  3. Price Range")
        try:
            ch = int(input("Choice: "))
            if ch == 1:
                term = input("Name: ")
                self.display_table(self.shop.search_by_name(term), f"Search: '{term}'")
            elif ch == 2:
                cat = self.get_category()
                if cat:
                    self.display_table(self.shop.search_by_category(cat), f"Search: {cat.value}")
            elif ch == 3:
                min_p = float(input("Min price: ₹"))
                max_p = float(input("Max price: ₹"))
                self.display_table(self.shop.search_by_price_range(min_p, max_p), f"₹{min_p} - ₹{max_p}")
        except:
            print("Invalid input.")

    def view_all(self):
        self.display_table(self.shop.view_all_sweets())

    def purchase(self):
        try:
            sid = int(input("Sweet ID: "))
            qty = int(input("Quantity: "))
            sweet, cost = self.shop.purchase_sweet(sid, qty)
            print(f"Purchased {qty} of {sweet.name} for ₹{cost:.2f}")
        except Exception as e:
            print(f"Error: {e}")

    def restock(self):
        try:
            sid = int(input("Sweet ID: "))
            qty = int(input("Quantity to add: "))
            sweet = self.shop.restock_sweet(sid, qty)
            print(f"Restocked {sweet.name}. New stock: {sweet.quantity}")
        except Exception as e:
            print(f"Error: {e}")

    def update_price(self):
        try:
            sid = int(input("Sweet ID: "))
            sweet = self.shop.get_sweet(sid)
            print(f"Current price: ₹{sweet.price}")
            new_price = float(input("New price: ₹"))
            self.shop.update_sweet_price(sid, new_price)
            print("Price updated.")
        except Exception as e:
            print(f"Error: {e}")

    def sort_sweets(self):
        print("\nSort by: 1. Name 2. Price ↑ 3. Price ↓ 4. Stock ↑ 5. Stock ↓")
        try:
            ch = int(input("Choice: "))
            if ch == 1:
                self.display_table(self.shop.sort_sweets_by_name(), "Sorted by Name")
            elif ch == 2:
                self.display_table(self.shop.sort_sweets_by_price(), "Price Low to High")
            elif ch == 3:
                self.display_table(self.shop.sort_sweets_by_price(True), "Price High to Low")
            elif ch == 4:
                self.display_table(self.shop.sort_sweets_by_quantity(), "Stock Low to High")
            elif ch == 5:
                self.display_table(self.shop.sort_sweets_by_quantity(True), "Stock High to Low")
        except:
            print("Invalid choice.")

    def reports(self):
        print("\n--- Reports ---")
        print(f"Total inventory value: ₹{self.shop.get_total_inventory_value():.2f}")
        lows = self.shop.get_low_stock_sweets()
        self.display_table(lows, "Low Stock Items") if lows else print("No low stock items.")
        print("\nCategory Summary:")
        summary = {}
        for s in self.shop.view_all_sweets():
            d = summary.setdefault(s.category, {'count': 0, 'value': 0})
            d['count'] += 1
            d['value'] += s.price * s.quantity
        for cat, d in summary.items():
            print(f"{cat.value:<15} {d['count']:>2} items, ₹{d['value']:>8.2f}")

    def run(self):
        print("Welcome to Sweet Shop Management System!")
        while True:
            self.display_menu()
            choice = input("Choice: ").strip()
            if choice == '1': self.add_sweet()
            elif choice == '2': self.delete_sweet()
            elif choice == '3': self.view_all()
            elif choice == '4': self.search_sweets()
            elif choice == '5': self.purchase()
            elif choice == '6': self.restock()
            elif choice == '7': self.update_price()
            elif choice == '8': self.sort_sweets()
            elif choice == '9': self.reports()
            elif choice == '10':
                self.save_data()
                break
            elif choice == '0':
                print("Exiting without saving.")
                break
            else:
                print("Invalid choice.")
            input("\nPress Enter to continue...")

def main():
    SweetShopCLI().run()

if __name__ == "__main__":
    main()
