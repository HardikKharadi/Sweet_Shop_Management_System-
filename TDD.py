"""
Test suite for Sweet Shop Management System
Following TDD principles with comprehensive test coverage
"""

import unittest
import tempfile
import os
from sweet_shop_manager import (
    SweetShopManager, Sweet, SweetCategory,
    InsufficientStockError, SweetNotFoundError, DuplicateSweetError
)


class TestSweet(unittest.TestCase):
    """Test cases for the Sweet class"""
    
    def test_create_sweet_valid_data(self):
        """Test creating a sweet with valid data"""
        sweet = Sweet(1001, "Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        
        self.assertEqual(sweet.id, 1001)
        self.assertEqual(sweet.name, "Kaju Katli")
        self.assertEqual(sweet.category, SweetCategory.NUT_BASED)
        self.assertEqual(sweet.price, 50.0)
        self.assertEqual(sweet.quantity, 20)
    
    def test_create_sweet_negative_price(self):
        """Test creating a sweet with negative price should raise ValueError"""
        with self.assertRaises(ValueError):
            Sweet(1001, "Test Sweet", SweetCategory.CHOCOLATE, -10.0, 20)
    
    def test_create_sweet_negative_quantity(self):
        """Test creating a sweet with negative quantity should raise ValueError"""
        with self.assertRaises(ValueError):
            Sweet(1001, "Test Sweet", SweetCategory.CHOCOLATE, 50.0, -5)
    
    def test_create_sweet_empty_name(self):
        """Test creating a sweet with empty name should raise ValueError"""
        with self.assertRaises(ValueError):
            Sweet(1001, "", SweetCategory.CHOCOLATE, 50.0, 20)
        
        with self.assertRaises(ValueError):
            Sweet(1001, "   ", SweetCategory.CHOCOLATE, 50.0, 20)
    
    def test_sweet_to_dict(self):
        """Test converting sweet to dictionary"""
        sweet = Sweet(1001, "Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        expected = {
            'id': 1001,
            'name': 'Kaju Katli',
            'category': 'Nut-Based',
            'price': 50.0,
            'quantity': 20
        }
        
        self.assertEqual(sweet.to_dict(), expected)
    
    def test_sweet_from_dict(self):
        """Test creating sweet from dictionary"""
        data = {
            'id': 1001,
            'name': 'Kaju Katli',
            'category': 'Nut-Based',
            'price': 50.0,
            'quantity': 20
        }
        
        sweet = Sweet.from_dict(data)
        
        self.assertEqual(sweet.id, 1001)
        self.assertEqual(sweet.name, "Kaju Katli")
        self.assertEqual(sweet.category, SweetCategory.NUT_BASED)
        self.assertEqual(sweet.price, 50.0)
        self.assertEqual(sweet.quantity, 20)


class TestSweetShopManager(unittest.TestCase):
    """Test cases for the SweetShopManager class"""
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.shop = SweetShopManager()
    
    def test_add_sweet_auto_id(self):
        """Test adding a sweet with auto-generated ID"""
        sweet = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        
        self.assertEqual(sweet.id, 1001)
        self.assertEqual(sweet.name, "Kaju Katli")
        self.assertEqual(sweet.category, SweetCategory.NUT_BASED)
        self.assertEqual(sweet.price, 50.0)
        self.assertEqual(sweet.quantity, 20)
    
    def test_add_multiple_sweets_auto_id(self):
        """Test adding multiple sweets with auto-generated IDs"""
        sweet1 = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        sweet2 = self.shop.add_sweet("Gulab Jamun", SweetCategory.MILK_BASED, 10.0, 50)
        
        self.assertEqual(sweet1.id, 1001)
        self.assertEqual(sweet2.id, 1002)
    
    def test_add_sweet_with_specific_id(self):
        """Test adding a sweet with a specific ID"""
        sweet = self.shop.add_sweet_with_id(2001, "Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        
        self.assertEqual(sweet.id, 2001)
        self.assertEqual(sweet.name, "Kaju Katli")
    
    def test_add_sweet_with_duplicate_id(self):
        """Test adding a sweet with duplicate ID should raise DuplicateSweetError"""
        self.shop.add_sweet_with_id(1001, "Sweet 1", SweetCategory.CHOCOLATE, 25.0, 10)
        
        with self.assertRaises(DuplicateSweetError):
            self.shop.add_sweet_with_id(1001, "Sweet 2", SweetCategory.CANDY, 30.0, 15)
    
    def test_delete_sweet_existing(self):
        """Test deleting an existing sweet"""
        sweet = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        
        self.shop.delete_sweet(sweet.id)
        
        with self.assertRaises(SweetNotFoundError):
            self.shop.get_sweet(sweet.id)
    
    def test_delete_sweet_nonexistent(self):
        """Test deleting a non-existent sweet should raise SweetNotFoundError"""
        with self.assertRaises(SweetNotFoundError):
            self.shop.delete_sweet(9999)
    
    def test_get_sweet_existing(self):
        """Test getting an existing sweet"""
        original_sweet = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        
        retrieved_sweet = self.shop.get_sweet(original_sweet.id)
        
        self.assertEqual(retrieved_sweet.id, original_sweet.id)
        self.assertEqual(retrieved_sweet.name, original_sweet.name)
    
    def test_get_sweet_nonexistent(self):
        """Test getting a non-existent sweet should raise SweetNotFoundError"""
        with self.assertRaises(SweetNotFoundError):
            self.shop.get_sweet(9999)
    
    def test_view_all_sweets_empty(self):
        """Test viewing all sweets when shop is empty"""
        sweets = self.shop.view_all_sweets()
        
        self.assertEqual(len(sweets), 0)
    
    def test_view_all_sweets_with_items(self):
        """Test viewing all sweets with items in shop"""
        sweet1 = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        sweet2 = self.shop.add_sweet("Gulab Jamun", SweetCategory.MILK_BASED, 10.0, 50)
        
        sweets = self.shop.view_all_sweets()
        
        self.assertEqual(len(sweets), 2)
        self.assertIn(sweet1, sweets)
        self.assertIn(sweet2, sweets)
    
    def test_search_by_name_exact_match(self):
        """Test searching by exact name match"""
        sweet = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        
        results = self.shop.search_by_name("Kaju Katli")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], sweet)
    
    def test_search_by_name_partial_match(self):
        """Test searching by partial name match"""
        sweet = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        
        results = self.shop.search_by_name("Kaju")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], sweet)
    
    def test_search_by_name_case_insensitive(self):
        """Test searching by name is case insensitive"""
        sweet = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        
        results = self.shop.search_by_name("kaju katli")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], sweet)
    
    def test_search_by_name_no_match(self):
        """Test searching by name with no matches"""
        self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        
        results = self.shop.search_by_name("Chocolate")
        
        self.assertEqual(len(results), 0)
    
    def test_search_by_category(self):
        """Test searching by category"""
        sweet1 = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        sweet2 = self.shop.add_sweet("Gulab Jamun", SweetCategory.MILK_BASED, 10.0, 50)
        sweet3 = self.shop.add_sweet("Almonds", SweetCategory.NUT_BASED, 100.0, 30)
        
        results = self.shop.search_by_category(SweetCategory.NUT_BASED)
        
        self.assertEqual(len(results), 2)
        self.assertIn(sweet1, results)
        self.assertIn(sweet3, results)
        self.assertNotIn(sweet2, results)
    
    def test_search_by_price_range(self):
        """Test searching by price range"""
        sweet1 = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        sweet2 = self.shop.add_sweet("Gulab Jamun", SweetCategory.MILK_BASED, 10.0, 50)
        sweet3 = self.shop.add_sweet("Almonds", SweetCategory.NUT_BASED, 100.0, 30)
        
        results = self.shop.search_by_price_range(20.0, 60.0)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], sweet1)
    
    def test_search_by_price_range_invalid(self):
        """Test searching by invalid price range should raise ValueError"""
        with self.assertRaises(ValueError):
            self.shop.search_by_price_range(100.0, 50.0)
    
    def test_purchase_sweet_valid(self):
        """Test purchasing sweets with valid quantity"""
        sweet = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        
        purchased_sweet, total_cost = self.shop.purchase_sweet(sweet.id, 5)
        
        self.assertEqual(purchased_sweet.quantity, 15)
        self.assertEqual(total_cost, 250.0)
    
    def test_purchase_sweet_insufficient_stock(self):
        """Test purchasing sweets with insufficient stock should raise InsufficientStockError"""
        sweet = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        
        with self.assertRaises(InsufficientStockError):
            self.shop.purchase_sweet(sweet.id, 25)
    
    def test_purchase_sweet_invalid_quantity(self):
        """Test purchasing sweets with invalid quantity should raise ValueError"""
        sweet = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        
        with self.assertRaises(ValueError):
            self.shop.purchase_sweet(sweet.id, 0)
        
        with self.assertRaises(ValueError):
            self.shop.purchase_sweet(sweet.id, -5)
    
    def test_purchase_sweet_nonexistent(self):
        """Test purchasing non-existent sweet should raise SweetNotFoundError"""
        with self.assertRaises(SweetNotFoundError):
            self.shop.purchase_sweet(9999, 1)
    
    def test_restock_sweet_valid(self):
        """Test restocking sweets with valid quantity"""
        sweet = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        
        restocked_sweet = self.shop.restock_sweet(sweet.id, 10)
        
        self.assertEqual(restocked_sweet.quantity, 30)
    
    def test_restock_sweet_invalid_quantity(self):
        """Test restocking sweets with invalid quantity should raise ValueError"""
        sweet = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        
        with self.assertRaises(ValueError):
            self.shop.restock_sweet(sweet.id, 0)
        
        with self.assertRaises(ValueError):
            self.shop.restock_sweet(sweet.id, -5)
    
    def test_restock_sweet_nonexistent(self):
        """Test restocking non-existent sweet should raise SweetNotFoundError"""
        with self.assertRaises(SweetNotFoundError):
            self.shop.restock_sweet(9999, 10)
    
    def test_update_sweet_price_valid(self):
        """Test updating sweet price with valid value"""
        sweet = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        
        updated_sweet = self.shop.update_sweet_price(sweet.id, 60.0)
        
        self.assertEqual(updated_sweet.price, 60.0)
    
    def test_update_sweet_price_invalid(self):
        """Test updating sweet price with invalid value should raise ValueError"""
        sweet = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)
        
        with self.assertRaises(ValueError):
            self.shop.update_sweet_price(sweet.id, -10.0)
    
    def test_update_sweet_price_nonexistent(self):
        """Test updating price of non-existent sweet should raise SweetNotFoundError"""
        with self.assertRaises(SweetNotFoundError):
            self.shop.update_sweet_price(9999, 60.0)
    
    def test_get_total_inventory_value(self):
        """Test calculating total inventory value"""
        self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 20)  # 1000
        self.shop.add_sweet("Gulab Jamun", SweetCategory.MILK_BASED, 10.0, 50)  # 500
        
        total_value = self.shop.get_total_inventory_value()
        
        self.assertEqual(total_value, 1500.0)
    
    def test_get_total_inventory_value_empty(self):
        """Test calculating total inventory value when empty"""
        total_value = self.shop.get_total_inventory_value()
        
        self.assertEqual(total_value, 0.0)
    
    def test_get_low_stock_sweets(self):
        """Test getting sweets with low stock"""
        sweet1 = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 3)
        sweet2 = self.shop.add_sweet("Gulab Jamun", SweetCategory.MILK_BASED, 10.0, 50)
        sweet3 = self.shop.add_sweet("Almonds", SweetCategory.NUT_BASED, 100.0, 5)
        
        low_stock_sweets = self.shop.get_low_stock_sweets()
        
        self.assertEqual(len(low_stock_sweets), 2)
        self.assertIn(sweet1, low_stock_sweets)
        self.assertIn(sweet3, low_stock_sweets)
        self.assertNotIn(sweet2, low_stock_sweets)
    
    def test_get_low_stock_sweets_custom_threshold(self):
        """Test getting sweets with low stock using custom threshold"""
        sweet1 = self.shop.add_sweet("Kaju Katli", SweetCategory.NUT_BASED, 50.0, 8)
        sweet2 = self.shop.add_sweet("Gulab Jamun", SweetCategory.MILK_BASED, 10.0, 50)
        
        low_stock_sweets = self.shop.get_low_stock_sweets(threshold=10)
        
        self.assertEqual(len(low_stock_sweets), 1)
        self.assertEqual(low_stock_sweets[0], sweet1)
    
    def test_sort_sweets_by_name(self):
        """Test sorting sweets by name"""
        sweet1 = self.shop.add_sweet("Zebra Cake", SweetCategory.PASTRY, 25.0, 10)
        sweet2 = self.shop.add_sweet("Apple Pie", SweetCategory.PASTRY, 30.0, 15)
        sweet3 = self.shop.add_sweet("Banana Bread", SweetCategory.PASTRY, 20.0, 20)
        
        sorted_sweets = self.shop.sort_sweets_by_name()
        
        self.assertEqual(sorted_sweets[0], sweet2)  # Apple Pie
        self.assertEqual(sorted_sweets[1], sweet3)  # Banana Bread
        self.assertEqual(sorted_sweets[2], sweet1)  # Zebra Cake
    
    def test_sort_sweets_by_price_ascending(self):
        """Test sorting sweets by price in ascending order"""
        import unittest
import sweet_shop_manager

class TestSweetShop(unittest.TestCase):
    def test_add_item(self):
        sweet_shop_manager.add_item("Test Sweet", 5, 25.0)
        items = sweet_shop_manager.get_all_items()
        self.assertTrue(any(i['name'] == "Test Sweet" for i in items))

    def test_delete_item(self):
        items = sweet_shop_manager.get_all_items()
        if items:
            last_id = items[-1]['id']
            sweet_shop_manager.delete_item(last_id)
            items_after = sweet_shop_manager.get_all_items()
            self.assertFalse(any(i['id'] == last_id for i in items_after))

if __name__ == '__main__':
    unittest.main()
