import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

class DataManager:
    def __init__(self, data_dir="/app/data"):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        self.transactions_file = os.path.join(data_dir, "transactions.json")
        self.audit_file = os.path.join(data_dir, "audit.json")
        self.orderbook_file = os.path.join(data_dir, "orderbook.json")
        
        os.makedirs(data_dir, exist_ok=True)
        
        self.users_db = self.load_users()
        self.transactions_db = self.load_transactions()
        self.audit_log = self.load_audit()
        self.order_book = self.load_orderbook()
    
    def load_users(self) -> Dict:
        """Load users from file or return empty dict"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading users: {e}")
        return {}
    
    def save_users(self):
        """Save users to file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users_db, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def load_transactions(self) -> List:
        """Load transactions from file or return empty list"""
        try:
            if os.path.exists(self.transactions_file):
                with open(self.transactions_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading transactions: {e}")
        return []
    
    def save_transactions(self):
        """Save transactions to file"""
        try:
            with open(self.transactions_file, 'w') as f:
                json.dump(self.transactions_db, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving transactions: {e}")
    
    def load_audit(self) -> List:
        """Load audit log from file or return empty list"""
        try:
            if os.path.exists(self.audit_file):
                with open(self.audit_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading audit log: {e}")
        return []
    
    def save_audit(self):
        """Save audit log to file"""
        try:
            with open(self.audit_file, 'w') as f:
                json.dump(self.audit_log, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving audit log: {e}")
    
    def load_orderbook(self) -> List:
        """Load order book from file or return empty list"""
        try:
            if os.path.exists(self.orderbook_file):
                with open(self.orderbook_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading order book: {e}")
        return []
    
    def save_orderbook(self):
        """Save order book to file"""
        try:
            with open(self.orderbook_file, 'w') as f:
                json.dump(self.order_book, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving order book: {e}")
    
    def add_user(self, user_id: str, user_data: Dict):
        """Add or update user"""
        self.users_db[user_id] = user_data
        self.save_users()
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        return self.users_db.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        for user in self.users_db.values():
            if user.get("username") == username:
                return user
        return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        for user in self.users_db.values():
            if user.get("email") == email:
                return user
        return None
    
    def add_transaction(self, transaction: Dict):
        """Add transaction"""
        self.transactions_db.append(transaction)
        self.save_transactions()
    
    def get_user_transactions(self, username: str) -> List:
        """Get transactions for a specific user"""
        return [
            t for t in self.transactions_db 
            if t.get("from_user") == username or t.get("to_user") == username
        ]
    
    def add_audit_log(self, log_entry: Dict):
        """Add audit log entry"""
        self.audit_log.append(log_entry)
        self.save_audit()
    
    def add_order(self, order: Dict):
        """Add order to order book"""
        self.order_book.append(order)
        self.save_orderbook()
    
    def backup_data(self):
        """Create backup of all data"""
        backup_dir = os.path.join(self.data_dir, "backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        backup_users_file = os.path.join(backup_dir, f"users_{timestamp}.json")
        with open(backup_users_file, 'w') as f:
            json.dump(self.users_db, f, indent=2, default=str)
        
        backup_transactions_file = os.path.join(backup_dir, f"transactions_{timestamp}.json")
        with open(backup_transactions_file, 'w') as f:
            json.dump(self.transactions_db, f, indent=2, default=str)
        
        backup_audit_file = os.path.join(backup_dir, f"audit_{timestamp}.json")
        with open(backup_audit_file, 'w') as f:
            json.dump(self.audit_log, f, indent=2, default=str)
        
        print(f"Data backup created: {timestamp}")
    
    def get_stats(self) -> Dict:
        """Get application statistics"""
        return {
            "total_users": len(self.users_db),
            "total_transactions": len(self.transactions_db),
            "total_audit_entries": len(self.audit_log),
            "total_orders": len(self.order_book),
            "last_backup": "N/A"
        } 