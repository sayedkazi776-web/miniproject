"""
Quick script to add your webcam to the system
Run: python add_webcam.py
"""
import requests
import json
import sys
import cv2

# Configuration
API_BASE = "http://localhost:5000/api"

print("\n" + "="*70)
print("🎥 Add Your Webcam to Crowd Density Monitoring System")
print("="*70)
print()

# Step 1: Test webcam access
print("[Step 1/4] Testing webcam access...")
print("-" * 70)

# Try to find available webcam
webcam_index = None
for i in range(3):  # Try indices 0, 1, 2
    print(f"  Testing webcam index {i}...", end=" ")
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print("✓ FOUND!")
            webcam_index = i
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            print(f"    Resolution: {width}x{height}")
            cap.release()
            break
        cap.release()
    print("✗ Not available")

if webcam_index is None:
    print("\n❌ ERROR: No webcam found!")
    print("\nTroubleshooting:")
    print("  • Make sure your webcam is connected")
    print("  • Check camera permissions in Windows Settings → Privacy → Camera")
    print("  • Close other apps that might be using the camera")
    print("  • Try restarting your computer")
    sys.exit(1)

print(f"\n✅ Webcam found at index {webcam_index}")

# Step 2: Get user credentials
print("\n[Step 2/4] Authentication required")
print("-" * 70)
EMAIL = input("Enter your email: ").strip()
PASSWORD = input("Enter your password: ").strip()

if not EMAIL or not PASSWORD:
    print("❌ Email and password are required!")
    sys.exit(1)

# Step 3: Login
print("\n[Step 3/4] Logging in...")
try:
    login_response = requests.post(f"{API_BASE}/auth/login", json={
        "email": EMAIL,
        "password": PASSWORD
    }, timeout=5)
except requests.exceptions.ConnectionError:
    print("❌ ERROR: Cannot connect to backend server!")
    print("\nMake sure the backend is running:")
    print("  cd backend")
    print("  python app.py")
    sys.exit(1)
except Exception as e:
    print(f"❌ ERROR: {e}")
    sys.exit(1)

if login_response.status_code != 200:
    error_msg = login_response.json().get('error', 'Unknown error')
    print(f"❌ Login failed: {error_msg}")
    print("\nTroubleshooting:")
    print("  • Check your email and password")
    print("  • Make sure you have registered an account")
    print("  • If you don't have an account, register at http://localhost:5000")
    sys.exit(1)

token = login_response.json().get('token')
if not token:
    print("❌ No token received from server")
    sys.exit(1)

print("✅ Login successful!")

# Step 4: Add Camera
print(f"\n[Step 4/4] Adding webcam to system...")
print("-" * 70)

# Get camera details
camera_name = input(f"Camera name (default: 'My Webcam'): ").strip() or "My Webcam"
camera_location = input(f"Location (default: 'Main Entrance'): ").strip() or "Main Entrance"

print(f"\nAdding camera:")
print(f"  Name: {camera_name}")
print(f"  Webcam Index: {webcam_index}")
print(f"  Location: {camera_location}")

headers = {"Authorization": f"Bearer {token}"}
camera_response = requests.post(
    f"{API_BASE}/cameras",
    headers=headers,
    json={
        "name": camera_name,
        "url": str(webcam_index),
        "location": camera_location
    },
    timeout=5
)

if camera_response.status_code == 201:
    camera_data = camera_response.json()
    print("\n" + "="*70)
    print("✅ SUCCESS! Webcam added successfully!")
    print("="*70)
    print(f"\nCamera Details:")
    print(f"  • Name: {camera_data['camera']['name']}")
    print(f"  • Webcam Index: {camera_data['camera']['url']}")
    print(f"  • Location: {camera_data['camera']['location']}")
    print(f"  • ID: {camera_data['camera']['id']}")
    print("\n" + "-"*70)
    print("Next Steps:")
    print("  1. Open http://localhost:5000 in your browser")
    print("  2. Login to your account")
    print("  3. Go to Dashboard")
    print("  4. Click on your camera card")
    print("  5. Click 'Start Stream' to begin monitoring!")
    print("="*70)
elif camera_response.status_code == 400:
    error = camera_response.json().get('error', 'Unknown error')
    print(f"\n❌ Failed to add camera: {error}")
    if "already exist" in error.lower():
        print("\n💡 Tip: A camera with this name already exists.")
        print("   You can:")
        print("   • Use a different name")
        print("   • Delete the old camera from the dashboard first")
        print("   • Or edit the existing camera")
elif camera_response.status_code == 401:
    print("\n❌ Unauthorized - Your session may have expired")
    print("   Please run this script again and login")
else:
    print(f"\n❌ Error: {camera_response.status_code}")
    try:
        print(camera_response.json())
    except:
        print(camera_response.text)



