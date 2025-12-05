"""
Database initialization script
Optional: Run this to initialize the database with sample data
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from models import init_db, User, Camera
from auth import hash_password
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

def initialize_database():
    """Initialize database with sample data"""
    mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://127.0.0.1:27017/crowd_density_db')
    
    print("Connecting to MongoDB...")
    init_db(mongodb_uri)
    print("Connected successfully!")
    
    # Create sample admin user
    admin_email = "admin@example.com"
    admin_password = "admin123"
    
    existing_user = User.find_by_email(admin_email)
    if not existing_user:
        password_hash = hash_password(admin_password)
        user_id = User.create(admin_email, password_hash, "Admin User")
        if user_id:
            print(f"Created admin user: {admin_email} / {admin_password}")
        else:
            print("Failed to create admin user")
    else:
        print(f"Admin user already exists: {admin_email}")
    
    # Create sample camera
    cameras = Camera.find_all()
    if len(cameras) == 0:
        camera_id = Camera.create("Sample Webcam", "0", "Main Entrance", existing_user['_id'] if existing_user else user_id)
        if camera_id:
            print(f"Created sample camera: Sample Webcam (using webcam index 0)")
        else:
            print("Failed to create sample camera")
    else:
        print(f"Found {len(cameras)} existing camera(s)")
    
    print("\nDatabase initialization complete!")
    print("\nYou can now:")
    print("1. Start the backend: cd backend && python app.py")
    print("2. Start the frontend: cd frontend && npm run dev")
    print("3. Login with: admin@example.com / admin123")

if __name__ == '__main__':
    initialize_database()

