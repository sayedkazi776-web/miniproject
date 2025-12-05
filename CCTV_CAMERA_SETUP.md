# 🎥 CCTV Camera Setup Guide - Complete Step-by-Step Process

## ✅ **Yes, You CAN Use CCTV Cameras!**

Your code **already supports** CCTV/IP cameras through RTSP (Real-Time Streaming Protocol). This guide will walk you through adding any CCTV camera to your system.

---

## 📋 **Table of Contents**
1. [Understanding Your CCTV Camera](#understanding-your-cctv-camera)
2. [Finding Your Camera's RTSP URL](#finding-your-cameras-rtsp-url)
3. [Testing Your RTSP Stream](#testing-your-rtsp-stream)
4. [Adding Camera to Your System](#adding-camera-to-your-system)
5. [Troubleshooting Common Issues](#troubleshooting-common-issues)
6. [Supported Camera Brands](#supported-camera-brands)

---

## 🔍 Step 1: Understanding Your CCTV Camera

Most modern CCTV/IP cameras support RTSP streaming. You need to find:
1. **Camera IP Address** (e.g., `192.168.1.100`)
2. **Username** (default is often `admin`)
3. **Password** (from your camera setup)
4. **RTSP Port** (usually `554`)
5. **Stream Path** (varies by brand)

---

## 🔎 Step 2: Finding Your Camera's RTSP URL

### **Method A: Check Camera Documentation**

Look at your camera's manual or manufacturer's website for RTSP URL format.

### **Method B: Access Camera Web Interface**

1. Find your camera's IP address:
   - Check your router's connected devices list
   - Or use `ipconfig` (Windows) / `ifconfig` (Linux/Mac) to see your network
   - Common ranges: `192.168.1.x`, `192.168.0.x`, `10.0.0.x`

2. Open browser and go to: `http://CAMERA_IP_ADDRESS` (e.g., `http://192.168.1.100`)

3. Login with username/password

4. Look for settings like:
   - "Streaming" or "Video Streaming"
   - "Network" or "Network Settings"
   - "RTSP Settings" or "RTSP Stream"
   - "Stream URL" or "Stream Path"

### **Method C: Common RTSP URL Formats by Brand**

#### **Hikvision Cameras:**
```
rtsp://username:password@192.168.1.64:554/Streaming/Channels/101
```
- Channel `101` = Main stream (high quality)
- Channel `102` = Sub stream (lower quality, better for streaming)

#### **Dahua Cameras:**
```
rtsp://admin:password@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0
```
- `subtype=0` = Main stream
- `subtype=1` = Sub stream

#### **Axis Cameras:**
```
rtsp://username:password@192.168.1.10/axis-media/media.amp
```
or
```
rtsp://username:password@192.168.1.10/mpeg4/media.amp
```

#### **Generic/Unbranded IP Cameras:**
Try these common patterns:
```
rtsp://username:password@192.168.1.100:554/stream1
rtsp://username:password@192.168.1.100:554/h264
rtsp://username:password@192.168.1.100:554/live
rtsp://username:password@192.168.1.100:554/ch1/stream1
rtsp://username:password@192.168.1.100:554/video
rtsp://username:password@192.168.1.100:554/11
```

#### **ONVIF-Compatible Cameras:**
Use ONVIF Device Manager tool to discover RTSP URLs:
1. Download: https://sourceforge.net/projects/onvifdm/
2. Scan network for cameras
3. Get RTSP URL from device settings

---

## 🧪 Step 3: Testing Your RTSP Stream

**IMPORTANT:** Always test your RTSP URL before adding to the system!

### **Test with VLC Media Player (Recommended):**

1. **Install VLC** (if not installed):
   - Download: https://www.videolan.org/vlc/

2. **Open VLC** and go to:
   - `Media` → `Open Network Stream` (or press `Ctrl+N`)

3. **Enter your RTSP URL**:
   - Example: `rtsp://admin:password123@192.168.1.100:554/stream1`

4. **Click "Play"**

5. **If video appears** → ✅ RTSP URL is correct!
6. **If error appears** → ❌ Need to fix URL or settings

### **Test with Python Script:**

Create a file `test_cctv.py` in your project root:

```python
import cv2

# Replace with your RTSP URL
RTSP_URL = "rtsp://username:password@192.168.1.100:554/stream1"

print(f"Testing RTSP stream: {RTSP_URL}")
print("Press 'q' to quit")

cap = cv2.VideoCapture(RTSP_URL)

if not cap.isOpened():
    print("❌ ERROR: Could not open RTSP stream")
    print("\nCommon fixes:")
    print("1. Check camera IP address")
    print("2. Check username/password")
    print("3. Check RTSP port (usually 554)")
    print("4. Check stream path")
    print("5. Try different stream path (stream1, stream2, etc.)")
    print("6. Check firewall settings")
else:
    print("✅ SUCCESS: RTSP stream opened!")
    print("Opening video window...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Failed to read frame")
            break
        
        cv2.imshow('Test CCTV', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
```

Run the test:
```bash
python test_cctv.py
```

---

## ➕ Step 4: Adding Camera to Your System

Once your RTSP URL works in VLC or test script:

### **Method A: Using Web Interface (Easiest)**

1. **Start your backend:**
   ```bash
   cd backend
   python app.py
   ```

2. **Open browser:** `http://localhost:5000`

3. **Login** to your account

4. **Click "Add Camera"** button

5. **Fill in the form:**
   - **Camera Name**: `Front Entrance CCTV`
   - **Video URL / Webcam Index**: `rtsp://admin:password123@192.168.1.100:554/stream1`
   - **Location**: `Main Entrance`
   
6. **Click "Add Camera"**

7. **Done!** Your CCTV appears on dashboard

### **Method B: Using Python Script**

1. **Edit `add_camera.py`:**
   ```python
   CAMERA_NAME = "My CCTV Camera"
   CAMERA_URL = "rtsp://admin:password123@192.168.1.100:554/stream1"
   CAMERA_LOCATION = "Front Entrance"
   ```

2. **Run the script:**
   ```bash
   python add_camera.py
   ```

3. **Enter your email and password** when prompted

4. **Camera added!**

### **Method C: Direct API Call**

```bash
curl -X POST http://localhost:5000/api/cameras \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "CCTV Camera 1",
    "url": "rtsp://admin:password123@192.168.1.100:554/stream1",
    "location": "Front Entrance"
  }'
```

---

## 🎬 Step 5: Using Your CCTV Camera

After adding:

1. **Go to Dashboard** - You'll see your CCTV camera card
2. **Click on the camera card**
3. **Click "Start Stream"** button
4. **Wait 5-10 seconds** for connection
5. **Video should appear!** 🎥

The system will:
- ✅ Show live CCTV feed
- ✅ Detect people in real-time
- ✅ Calculate crowd density
- ✅ Trigger alerts if density is high
- ✅ Log data to database

---

## 🔧 Troubleshooting Common Issues

### **Issue 1: "Could not open video source"**

**Solutions:**
- ✅ Test RTSP URL in VLC first
- ✅ Check username/password are correct
- ✅ Verify camera IP address is reachable
- ✅ Try different stream path (e.g., stream1 → stream2)
- ✅ Check if camera supports RTSP
- ✅ Ping camera: `ping 192.168.1.100`

### **Issue 2: "Connection timeout"**

**Solutions:**
- ✅ Check network connectivity
- ✅ Verify camera is powered on
- ✅ Check firewall settings
- ✅ Ensure RTSP port (554) is open
- ✅ Try from camera's web interface first

### **Issue 3: "Authentication failed"**

**Solutions:**
- ✅ Double-check username and password
- ✅ Try default credentials (admin/admin, admin/12345, etc.)
- ✅ Reset camera to factory defaults if needed
- ✅ Check if password has special characters that need encoding

### **Issue 4: "Video freezes or laggy"**

**Solutions:**
- ✅ Use sub-stream (lower quality) instead of main stream
- ✅ Reduce camera resolution in camera settings
- ✅ Check network bandwidth
- ✅ Use wired Ethernet instead of WiFi
- ✅ Close other applications using bandwidth

### **Issue 5: "Stream disconnects after a while"**

**Solutions:**
- ✅ Update OpenCV: `pip install --upgrade opencv-python`
- ✅ Some cameras have timeout settings - disable them
- ✅ Check camera firmware is up to date
- ✅ Try adding `?tcp=1` to RTSP URL for some cameras

### **Issue 6: "No video feed but RTSP works in VLC"**

**Solutions:**
- ✅ Restart backend server
- ✅ Check backend logs for errors
- ✅ Try using TCP transport instead of UDP
- ✅ Some cameras need specific codec settings

---

## 📊 Supported Camera Brands

Your system works with **ANY RTSP-compatible camera**, including:

### **Major Brands:**
- ✅ **Hikvision** - Excellent compatibility
- ✅ **Dahua** - Excellent compatibility
- ✅ **Axis** - Excellent compatibility
- ✅ **Uniview** - Good compatibility
- ✅ **Hanwha Techwin (Samsung)** - Good compatibility
- ✅ **Bosch** - Good compatibility
- ✅ **Pelco** - Good compatibility
- ✅ **Panasonic** - Good compatibility
- ✅ **Sony** - Good compatibility

### **Budget/Unbranded:**
- ✅ Most generic IP cameras with RTSP
- ✅ Reolink cameras
- ✅ Foscam cameras
- ✅ TP-Link cameras
- ✅ Most ONVIF-compatible cameras

### **Not Supported:**
- ❌ Cameras that only support proprietary protocols (without RTSP)
- ❌ Some very old analog cameras (need RTSP encoder)
- ❌ Cloud-only cameras without local RTSP

---

## 🎯 Quick Reference: RTSP URL Format

```
General Format:
rtsp://USERNAME:PASSWORD@IP_ADDRESS:PORT/STREAM_PATH

Example:
rtsp://admin:mypassword@192.168.1.100:554/stream1

Components:
- USERNAME: Camera login username (often "admin")
- PASSWORD: Camera login password
- IP_ADDRESS: Camera IP on your network
- PORT: RTSP port (usually 554)
- STREAM_PATH: Stream path (varies by brand)
```

---

## 📝 Example RTSP URLs

Here are some real examples you can adapt:

```bash
# Hikvision Camera
rtsp://admin:12345@192.168.1.64:554/Streaming/Channels/101

# Dahua Camera  
rtsp://admin:admin@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0

# Generic IP Camera
rtsp://user:pass@192.168.0.50:554/stream1

# Axis Camera
rtsp://root:pass@10.0.0.100/axis-media/media.amp

# UniFi Camera
rtsp://192.168.1.100:7447/[SECRET]/live

# Reolink Camera
rtsp://admin:password@192.168.1.10:554/h264Preview_01_main
```

---

## ✅ Final Checklist

Before adding a CCTV camera:

- [ ] Camera is powered on and connected to network
- [ ] Camera IP address is known
- [ ] Camera username and password are known
- [ ] RTSP URL has been tested in VLC Media Player
- [ ] RTSP stream shows video successfully in VLC
- [ ] Backend server is running
- [ ] You're logged into the web interface

---

## 🆘 Still Having Issues?

If you're still having problems:

1. **Test with simpler setup**: Try adding a webcam first (just use `0` as URL)
2. **Check logs**: Look at backend console for error messages
3. **Database check**: Run `python backend/view_database.py` to see cameras
4. **Network test**: Try pinging camera from the same computer running backend
5. **Camera reset**: Some cameras need to be reset to factory defaults

---

## 📞 Need More Help?

Common questions answered:

**Q: Can I use multiple CCTV cameras?**
A: Yes! Add each one separately with different names.

**Q: Can I mix webcams and CCTV cameras?**
A: Yes! The system supports any combination.

**Q: Will CCTV work over the internet?**
A: Yes, if you configure port forwarding, but local network is recommended.

**Q: What about security?**
A: RTSP URLs with passwords are stored in your database. Keep your MongoDB secure.

**Q: Can I change camera settings after adding?**
A: Yes, edit camera settings in the web interface or delete and re-add.

---

## 🎉 You're All Set!

Your CCTV camera should now be working with the crowd density monitoring system. Enjoy real-time monitoring! 🎥📊

---

**Last Updated:** 2024  
**System Version:** Crowd Density Monitoring v1.0  
**Compatibility:** All RTSP-compatible cameras


