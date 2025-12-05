"""
Quick script to add a camera via API
Run: python add_camera.py
"""
import requests
import json
import sys

# Configuration
API_BASE = "http://localhost:5000/api"
EMAIL = input("Enter your email: ").strip()
PASSWORD = input("Enter your password: ").strip()

# Camera details
CAMERA_NAME = "My Webcam"
CAMERA_URL = "0"  # First webcam - change to 1, 2, etc. if needed
CAMERA_LOCATION = "Main Entrance"

print("\n" + "="*60)
print("Adding Camera via API")
print("="*60)

# Step 1: Login
print("\n[1/2] Logging in...")
login_response = requests.post(f"{API_BASE}/auth/login", json={
    "email": EMAIL,
    "password": PASSWORD
})

if login_response.status_code != 200:
    print(f"✗ Login failed: {login_response.json().get('error', 'Unknown error')}")
    sys.exit(1)

token = login_response.json().get('token')
if not token:
    print("✗ No token received")
    sys.exit(1)

print("✓ Login successful!")

# Step 2: Add Camera
print(f"\n[2/2] Adding camera: {CAMERA_NAME} (URL: {CAMERA_URL})...")
headers = {"Authorization": f"Bearer {token}"}
camera_response = requests.post(
    f"{API_BASE}/cameras",
    headers=headers,
    json={
        "name": CAMERA_NAME,
        "url": CAMERA_URL,
        "location": CAMERA_LOCATION
    }
)

if camera_response.status_code == 201:
    camera_data = camera_response.json()
    print("✓ Camera added successfully!")
    print(f"\nCamera Details:")
    print(f"  Name: {camera_data['camera']['name']}")
    print(f"  URL: {camera_data['camera']['url']}")
    print(f"  Location: {camera_data['camera']['location']}")
    print(f"  ID: {camera_data['camera']['id']}")
    print("\n" + "="*60)
    print("You can now use this camera in the dashboard!")
    print("="*60)
elif camera_response.status_code == 400:
    error = camera_response.json().get('error', 'Unknown error')
    print(f"✗ Failed to add camera: {error}")
    if "already exist" in error.lower():
        print("\nTip: Camera name might already exist. Try a different name.")
elif camera_response.status_code == 401:
    print("✗ Unauthorized - check your credentials")
else:
    print(f"✗ Error: {camera_response.status_code}")
    print(camera_response.text)

