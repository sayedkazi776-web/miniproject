"""
Diagnostic script to test authentication and database connection
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import init_db, User
import models
from auth import hash_password, verify_password
from dotenv import load_dotenv

load_dotenv()

def test_database_connection():
    """Test if MongoDB is connected"""
    print("=" * 70)
    print("Testing Database Connection")
    print("=" * 70)
    
    try:
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://127.0.0.1:27017/crowd_density_db')
        print(f"MongoDB URI: {mongodb_uri}")
        
        init_db(mongodb_uri)
        print("[OK] Database connection successful!")
        
        # Test if we can access the database
        if models.db is None:
            print("[ERROR] Database object is None!")
            return False
        
        # Test if collections exist
        collections = models.db.db.list_collection_names()
        print(f"[OK] Found collections: {collections}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        print("\nPossible solutions:")
        print("1. Make sure MongoDB is running:")
        print("   - Windows: Check Services or run 'net start MongoDB'")
        print("   - Linux/Mac: sudo systemctl start mongod")
        print("2. Check if MongoDB is listening on port 27017")
        print("3. Verify MONGODB_URI in .env file")
        return False

def test_user_operations():
    """Test user creation and retrieval"""
    print("\n" + "=" * 70)
    print("Testing User Operations")
    print("=" * 70)
    
    try:
        # Test creating a user
        test_email = "test@example.com"
        test_password = "test123"
        test_name = "Test User"
        
        print(f"Creating test user: {test_email}")
        
        # Check if user already exists
        existing = User.find_by_email(test_email)
        if existing:
            print(f"[OK] User {test_email} already exists")
            print("   Testing password verification...")
            if verify_password(test_password, existing['password_hash']):
                print("   [OK] Password verification successful")
            else:
                print("   [ERROR] Password verification failed")
        else:
            password_hash = hash_password(test_password)
            user_id = User.create(test_email, password_hash, test_name)
            
            if user_id:
                print(f"[OK] User created successfully! ID: {user_id}")
            else:
                print("[ERROR] Failed to create user (possibly duplicate)")
        
        # Test finding user
        found_user = User.find_by_email(test_email)
        if found_user:
            print(f"[OK] User found: {found_user['email']}")
            return True
        else:
            print("[ERROR] User not found after creation")
            return False
            
    except Exception as e:
        print(f"[ERROR] User operation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_admin_user():
    """Test if admin user exists and can login"""
    print("\n" + "=" * 70)
    print("Testing Admin User")
    print("=" * 70)
    
    admin_email = "admin@example.com"
    admin_password = "admin123"
    
    user = User.find_by_email(admin_email)
    
    if user:
        print(f"[OK] Admin user found: {admin_email}")
        print("   Testing password verification...")
        if verify_password(admin_password, user['password_hash']):
            print(f"   [OK] Password '{admin_password}' is correct!")
            print(f"   [OK] You can login with: {admin_email} / {admin_password}")
            return True
        else:
            print(f"   [ERROR] Password '{admin_password}' is incorrect!")
            print("   The password hash in database doesn't match.")
            print("   Solution: Run 'python db/init_db.py' to reset admin user")
            return False
    else:
        print(f"[ERROR] Admin user not found: {admin_email}")
        print("   Solution: Run 'python db/init_db.py' to create admin user")
        return False

def main():
    """Run all diagnostic tests"""
    print("\n" + "=" * 70)
    print("AUTHENTICATION DIAGNOSTIC TOOL")
    print("=" * 70)
    print()
    
    # Test 1: Database connection
    db_ok = test_database_connection()
    if not db_ok:
        print("\n[WARNING] Database connection failed. Fix this first!")
        return
    
    # Test 2: User operations
    user_ops_ok = test_user_operations()
    
    # Test 3: Admin user
    admin_ok = test_admin_user()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Database Connection: {'[OK]' if db_ok else '[FAILED]'}")
    print(f"User Operations: {'[OK]' if user_ops_ok else '[FAILED]'}")
    print(f"Admin User: {'[OK]' if admin_ok else '[FAILED]'}")
    
    if db_ok and user_ops_ok and admin_ok:
        print("\n[OK] All tests passed! Authentication should work.")
    else:
        print("\n[WARNING] Some tests failed. Please fix the issues above.")
    
    print()

if __name__ == '__main__':
    main()

