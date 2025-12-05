"""
Simple script to view database contents
Run: python view_database.py
"""
from models import init_db, User, Camera, DensityLog
from dotenv import load_dotenv
import os
from bson import ObjectId
from datetime import datetime

load_dotenv()

# Initialize database
mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://127.0.0.1:27017/crowd_density_db')
init_db(mongodb_uri)

print("=" * 60)
print("CROWD DENSITY MONITORING - DATABASE VIEWER")
print("=" * 60)
print()

# Import db instance
from models import db

# View Users
print("=" * 60)
print("USERS")
print("=" * 60)
users = list(db.db.users.find())
if users:
    for user in users:
        print(f"ID: {user['_id']}")
        print(f"  Email: {user['email']}")
        print(f"  Name: {user.get('name', 'N/A')}")
        print(f"  Created: {user.get('created_at', 'N/A')}")
        print()
else:
    print("No users found")
    print()

# View Cameras
print("=" * 60)
print("CAMERAS")
print("=" * 60)
cameras = Camera.find_all()
if cameras:
    for cam in cameras:
        print(f"ID: {cam['_id']}")
        print(f"  Name: {cam['name']}")
        print(f"  Location: {cam.get('location', 'N/A')}")
        print(f"  URL: {cam['url']}")
        print(f"  Owner: {cam.get('owner_id', 'N/A')}")
        print(f"  Created: {cam.get('created_at', 'N/A')}")
        print()
else:
    print("No cameras found")
    print()

# View Density Logs
print("=" * 60)
print("DENSITY LOGS (Last 20)")
print("=" * 60)
logs = list(db.db.density_logs.find().sort('timestamp', -1).limit(20))
if logs:
    for log in logs:
        print(f"ID: {log['_id']}")
        print(f"  Camera: {log['camera_id']}")
        print(f"  Timestamp: {log['timestamp']}")
        print(f"  People Count: {log['person_count']}")
        print(f"  Density Value: {log['density_value']:.3f}")
        print(f"  Density per sqm: {log.get('density_per_sqm', 'N/A')}")
        print(f"  Alert Triggered: {log.get('alert_triggered', False)}")
        print()
else:
    print("No density logs found")
    print()

# Statistics
print("=" * 60)
print("STATISTICS")
print("=" * 60)
total_users = db.db.users.count_documents({})
total_cameras = db.db.cameras.count_documents({})
total_logs = db.db.density_logs.count_documents({})
alert_count = db.db.density_logs.count_documents({'alert_triggered': True})

print(f"Total Users: {total_users}")
print(f"Total Cameras: {total_cameras}")
print(f"Total Density Logs: {total_logs}")
print(f"Total Alerts: {alert_count}")
print()

# Per-camera statistics
if cameras:
    print("=" * 60)
    print("PER-CAMERA STATISTICS")
    print("=" * 60)
    for cam in cameras:
        cam_id = cam['_id']
        cam_logs = list(db.db.density_logs.find({'camera_id': cam_id}))
        if cam_logs:
            avg_density = sum(log['density_value'] for log in cam_logs) / len(cam_logs)
            max_density = max(log['density_value'] for log in cam_logs)
            avg_people = sum(log['person_count'] for log in cam_logs) / len(cam_logs)
            alerts = sum(1 for log in cam_logs if log.get('alert_triggered', False))
            
            print(f"Camera: {cam['name']}")
            print(f"  Total Logs: {len(cam_logs)}")
            print(f"  Average Density: {avg_density:.3f}")
            print(f"  Max Density: {max_density:.3f}")
            print(f"  Average People: {avg_people:.1f}")
            print(f"  Alerts: {alerts}")
            print()

print("=" * 60)
print("View complete!")
print("=" * 60)

