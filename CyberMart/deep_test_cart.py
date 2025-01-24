#!/usr/bin/env python3
"""
Deep Test for vuln-cart E-commerce Flow
Tests complete shopping process: register -> login -> browse -> cart -> checkout
"""

import requests
import json
import time
import re
from urllib.parse import urljoin

class VulnCartDeepTest:
    def __init__(self):
        self.base_url = "http://localhost:5002"
        self.session = requests.Session()
        self.cart_items = []
        self.order_id = None
        
    def test_homepage(self):
        """Test homepage accessibility"""
        print("🏠 Testing homepage...")
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                print("✅ Homepage accessible")
                return True
            else:
                print(f"❌ Homepage failed - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Homepage error: {e}")
            return False
    
    def test_products_page(self):
        """Test products listing page"""
        print("🛍️ Testing products page...")
        try:
            response = self.session.get(f"{self.base_url}/products")
            if response.status_code == 200:
                print("✅ Products page accessible")
                # Check if products are displayed
                if "product" in response.text.lower() or "price" in response.text.lower():
                    print("✅ Products found on page")
                    return True
                else:
                    print("⚠️ No products found on page")
                    return False
            else:
                print(f"❌ Products page failed - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Products page error: {e}")
            return False
    
    def test_user_registration(self):
        """Test user registration"""
        print("👤 Testing user registration...")
        registration_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
            "confirm_password": "testpass123",
            "payment_info": "4111111111111111"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/register", data=registration_data)
            if response.status_code in [200, 302]:
                print("✅ User registration successful")
                return True
            else:
                print(f"❌ User registration failed - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ User registration error: {e}")
            return False
    
    def test_user_login(self):
        """Test user login"""
        print("🔐 Testing user login...")
        login_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/login", data=login_data, allow_redirects=False)
            if response.status_code == 302:
                print("✅ User login successful")
                # Follow redirect to complete login
                redirect_url = response.headers.get('Location')
                if redirect_url:
                    self.session.get(f"{self.base_url}{redirect_url}")
                return True
            else:
                print(f"❌ User login failed - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ User login error: {e}")
            return False
    
    def test_product_details(self):
        """Test product details page"""
        print("📦 Testing product details...")
        try:
            # Try to access a specific product (ID 1)
            response = self.session.get(f"{self.base_url}/product/1")
            if response.status_code == 200:
                print("✅ Product details page accessible")
                return True
            else:
                print(f"❌ Product details failed - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Product details error: {e}")
            return False
    
    def test_add_to_cart(self):
        """Test adding items to cart"""
        print("🛒 Testing add to cart...")
        try:
            # Add product ID 1 to cart
            cart_data = {
                "product_id": "1",
                "quantity": "2"
            }
            response = self.session.post(f"{self.base_url}/add_to_cart", data=cart_data)
            if response.status_code in [200, 302]:
                print("✅ Add to cart successful")
                self.cart_items.append({"product_id": 1, "quantity": 2})
                return True
            else:
                print(f"❌ Add to cart failed - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Add to cart error: {e}")
            return False
    
    def test_view_cart(self):
        """Test viewing cart"""
        print("🛒 Testing view cart...")
        try:
            response = self.session.get(f"{self.base_url}/cart")
            if response.status_code == 200:
                print("✅ Cart page accessible")
                return True
            else:
                print(f"❌ Cart page failed - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cart page error: {e}")
            return False
    
    def test_checkout(self):
        """Test checkout process"""
        print("💳 Testing checkout...")
        try:
            checkout_data = {
                "name": "Test User",
                "email": "testuser@example.com",
                "address": "123 Test St",
                "city": "Test City",
                "postal_code": "12345",
                "card_number": "4111111111111111",
                "expiry": "12/25",
                "cvv": "123"
            }
            response = self.session.post(f"{self.base_url}/checkout", data=checkout_data)
            if response.status_code in [200, 302]:
                print("✅ Checkout successful")
                
                # Extract order ID if available
                order_id_match = re.search(r'order[:\s]*(\d+)', response.text, re.IGNORECASE)
                if order_id_match:
                    self.order_id = order_id_match.group(1)
                    print(f"✅ Order ID: {self.order_id}")
                
                return True
            else:
                print(f"❌ Checkout failed - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Checkout error: {e}")
            return False
    
    def test_order_history(self):
        """Test order history page"""
        print("📋 Testing order history...")
        try:
            response = self.session.get(f"{self.base_url}/orders")
            if response.status_code == 200:
                print("✅ Order history page accessible")
                return True
            else:
                print(f"❌ Order history failed - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Order history error: {e}")
            return False
    
    def test_search_functionality(self):
        """Test product search"""
        print("🔍 Testing product search...")
        try:
            response = self.session.get(f"{self.base_url}/search?q=laptop")
            if response.status_code == 200:
                print("✅ Search functionality accessible")
                return True
            else:
                print(f"❌ Search failed - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Search error: {e}")
            return False
    
    def test_admin_panel(self):
        """Test admin panel access"""
        print("👑 Testing admin panel...")
        try:
            response = self.session.get(f"{self.base_url}/admin")
            if response.status_code == 200:
                print("✅ Admin panel accessible")
                return True
            else:
                print(f"❌ Admin panel failed - Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Admin panel error: {e}")
            return False
    
    def run_complete_test(self):
        """Run complete e-commerce flow test"""
        print("🚀 Starting Deep Test for vuln-cart E-commerce Flow")
        print("=" * 60)
        
        tests = [
            ("Homepage", self.test_homepage),
            ("Products Page", self.test_products_page),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("Product Details", self.test_product_details),
            ("Add to Cart", self.test_add_to_cart),
            ("View Cart", self.test_view_cart),
            ("Checkout", self.test_checkout),
            ("Order History", self.test_order_history),
            ("Search Functionality", self.test_search_functionality),
            ("Admin Panel", self.test_admin_panel)
        ]
        
        results = {}
        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            try:
                result = test_func()
                results[test_name] = result
            except Exception as e:
                print(f"❌ {test_name} crashed: {e}")
                results[test_name] = False
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name}: {status}")
        
        print(f"\nOverall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if self.order_id:
            print(f"📋 Order ID: {self.order_id}")
        
        return results

if __name__ == "__main__":
    tester = VulnCartDeepTest()
    tester.run_complete_test() 