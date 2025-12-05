# 📹 Complete Guide: Adding CCTV Cameras to Your System

This comprehensive guide will walk you through adding any type of camera (webcam, IP camera, CCTV) to your Crowd Density Monitoring system.

---

## 🎯 Quick Start: Add Your Webcam (Easiest Method)

### Option 1: Automated Script (Recommended)

1. **Make sure backend is running:**
   ```bash
   cd backend
   python app.py
   ```

2. **In a NEW terminal, run:**
   ```bash
   python add_webcam.py
   ```

3. **Follow the prompts:**
   - Enter your email and password
   - Enter camera name (or press Enter for default)
   - Enter location (or press Enter for default)

4. **Done!** Your webcam is now added and ready to use.

### Option 2: Web Interface

1. **Start the application:**
   ```bash
   cd backend
   python app.py
   ```

2. **Open browser:** `http://localhost:5000`

3. **Login** with your account

4. **Go to Dashboard** → Click **"Add Camera"** button

5. **Fill in the form:**
   - **Camera Name**: `My Webcam` (or any name)
   - **Video URL / Webcam Index**: `0` (for first webcam)
   - **Location**: `Main Entrance` (or any location)

6. **Click "Add Camera"**

7. **Done!** Your camera card will appear on the dashboard.

---

## 🔍 Finding Your Webcam Index

### Windows

**Method 1: Test Script**
```bash
python test_cctv.py
# Enter: 0
# Press 'q' to quit if video appears
```

**Method 2: PowerShell**
```powershell
Get-CimInstance Win32_PnPEntity | Where-Object {$_.Name -like "*camera*" -or $_.Name -like "*webcam*"}
```

**Method 3: Try Different Indices**
- Start with `0` (most common)
- If `0` doesn't work, try `1`, `2`, `3`, etc.

### Common Webcam Indices

- `0` = First/default webcam (most common)
- `1` = Second webcam (if you have multiple)
- `2` = Third webcam
- etc.

---

## 🌐 Adding IP Cameras / CCTV Cameras (RTSP)

### Step 1: Find Your Camera's RTSP URL

Most IP cameras use RTSP (Real-Time Streaming Protocol). You need to find:
- Camera IP address
- Username and password
- RTSP port (usually 554)
- Stream path

### Step 2: Common RTSP URL Formats by Brand

#### Hikvision Cameras
```
rtsp://admin:password@192.168.1.64:554/Streaming/Channels/101
```
- **Channel 101** = Main stream (high quality)
- **Channel 102** = Sub stream (lower quality, better for streaming)

#### Dahua Cameras
```
rtsp://admin:password@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0
```
- **subtype=0** = Main stream
- **subtype=1** = Sub stream

#### Generic IP Cameras
```
rtsp://username:password@192.168.1.100:554/stream1
rtsp://username:password@192.168.1.100:554/h264
rtsp://username:password@192.168.1.100:554/live
```

### Step 3: Test Your RTSP URL First

**Before adding to the system, test the RTSP URL:**

1. **Using VLC Media Player:**
   - Open VLC
   - Media → Open Network Stream
   - Enter your RTSP URL
   - Click Play
   - If video appears, the URL is correct!

2. **Using Test Script:**
   ```bash
   python test_cctv.py
   # Enter your RTSP URL when prompted
   # Press 'q' to quit if video appears
   ```

### Step 4: Add Camera to System

**Method 1: Web Interface**
1. Go to Dashboard → Click "Add Camera"
2. Fill in:
   - **Name**: `Front Entrance Camera` (or any name)
   - **Video URL**: `rtsp://admin:password@192.168.1.64:554/Streaming/Channels/101`
   - **Location**: `Front Entrance` (or any location)
3. Click "Add Camera"

**Method 2: Using Script**
1. Edit `add_camera.py`:
   ```python
   CAMERA_NAME = "Front Entrance Camera"
   CAMERA_URL = "rtsp://admin:password@192.168.1.64:554/Streaming/Channels/101"
   CAMERA_LOCATION = "Front Entrance"
   ```
2. Run: `python add_camera.py`

---

## 🔧 Finding Your Camera's IP Address

### Method 1: Camera's Web Interface

1. **Connect to camera's network** (same WiFi/LAN)
2. **Open camera's web interface** (usually shown in camera manual)
   - Common: `http://192.168.1.64` or `http://192.168.0.64`
3. **Login** with admin credentials
4. **Look for RTSP settings** or **Network settings**
5. **Note the IP address and RTSP port**

### Method 2: Network Scanner

**Windows (PowerShell):**
```powershell
# Scan local network for devices
1..254 | ForEach-Object { 
    $ip = "192.168.1.$_"
    if (Test-Connection -ComputerName $ip -Count 1 -Quiet) {
        Write-Host "$ip is alive"
    }
}
```

**Using Router Admin Panel:**
1. Login to your router (usually `192.168.1.1` or `192.168.0.1`)
2. Go to "Connected Devices" or "DHCP Clients"
3. Look for camera device name
4. Note the IP address

### Method 3: Camera's Default IP

Check camera manual for default IP. Common defaults:
- `192.168.1.64`
- `192.168.0.64`
- `192.168.1.108`
- `192.168.0.108`

---

## 🔐 Camera Credentials

### Default Credentials (Change These!)

**Hikvision:**
- Username: `admin`
- Password: `12345` or `admin` (check manual)

**Dahua:**
- Username: `admin`
- Password: `admin` (check manual)

**⚠️ IMPORTANT:** Always change default passwords for security!

### Finding/Resetting Credentials

1. **Check camera manual** or sticker on camera
2. **Use camera's web interface** to reset password
3. **Contact camera manufacturer** if needed

---

## 📝 Complete Example: Adding a Hikvision Camera

### Step-by-Step:

1. **Find camera IP:**
   - Check router admin panel → Connected devices
   - Found: `192.168.1.64`

2. **Test camera access:**
   - Open browser: `http://192.168.1.64`
   - Login with admin credentials
   - Camera is accessible ✓

3. **Find RTSP URL:**
   - Check camera manual or web interface
   - Format: `rtsp://admin:password@192.168.1.64:554/Streaming/Channels/101`

4. **Test RTSP URL:**
   ```bash
   python test_cctv.py
   # Enter: rtsp://admin:password@192.168.1.64:554/Streaming/Channels/101
   # If video appears, URL is correct ✓
   ```

5. **Add to system:**
   - Dashboard → Add Camera
   - Name: `Hikvision Front Camera`
   - URL: `rtsp://admin:password@192.168.1.64:554/Streaming/Channels/101`
   - Location: `Front Entrance`
   - Click "Add Camera"

6. **Start monitoring:**
   - Click on camera card
   - Click "Start Stream"
   - Video should appear! 🎥

---

## 🎬 Adding Video Files (For Testing)

You can also use video files for testing without a camera:

1. **Add Camera:**
   - Name: `Test Video`
   - URL: `C:\Videos\test.mp4` (Windows) or `/path/to/video.mp4` (Linux/Mac)
   - Location: `Testing`

2. **Supported formats:**
   - `.mp4`
   - `.avi`
   - `.mov`
   - `.mkv`
   - Any format supported by OpenCV

---

## 🔧 Troubleshooting

### Webcam Issues

**"Could not open webcam"**
- ✅ Try different index: `0`, `1`, `2`, etc.
- ✅ Check camera permissions:
  - Windows: Settings → Privacy → Camera → Allow apps to access camera
  - Mac: System Preferences → Security → Camera
  - Linux: Add user to video group: `sudo usermod -a -G video $USER`
- ✅ Close other apps using the camera (Zoom, Teams, etc.)
- ✅ Restart computer if needed

**"Camera not found"**
- ✅ Make sure webcam is connected (USB)
- ✅ Check device manager (Windows) for camera device
- ✅ Try unplugging and replugging USB cable

### RTSP/IP Camera Issues

**"Could not open video source"**
- ✅ Test RTSP URL in VLC first
- ✅ Verify camera IP address is correct
- ✅ Check username and password
- ✅ Ensure camera is on same network
- ✅ Try different stream path (stream1, stream2, etc.)
- ✅ Check RTSP port (usually 554)
- ✅ Verify camera is powered on

**"Stream disconnected"**
- ✅ Check network connection
- ✅ Verify camera is still powered on
- ✅ Try using TCP transport: Add `?tcp=1` to URL
- ✅ Check firewall settings

**"Slow or laggy stream"**
- ✅ Use sub-stream instead of main stream (lower quality, faster)
- ✅ For Hikvision: Use channel 102 instead of 101
- ✅ For Dahua: Use `subtype=1` instead of `subtype=0`
- ✅ Reduce camera resolution in camera settings

### General Issues

**"Camera name already exists"**
- ✅ Use a different name
- ✅ Delete the old camera first
- ✅ Edit existing camera instead

**"Invalid camera URL"**
- ✅ For webcam: Must be a number (`0`, `1`, `2`, etc.)
- ✅ For RTSP: Must start with `rtsp://`
- ✅ No spaces or special characters (except in password)

---

## 📋 Camera URL Format Reference

### Webcam
```
0          # First webcam
1          # Second webcam
2          # Third webcam
```

### RTSP (IP Camera)
```
rtsp://username:password@ip:port/stream-path
```

### Video File
```
C:\Videos\test.mp4           # Windows absolute path
/path/to/video.mp4           # Linux/Mac absolute path
```

---

## ✅ Best Practices

1. **Test First:** Always test camera URL with `test_cctv.py` or VLC before adding to system
2. **Use Descriptive Names:** Name cameras clearly (e.g., "Front Entrance", "Parking Lot")
3. **Secure Credentials:** Change default camera passwords
4. **Network Security:** Use strong passwords for camera access
5. **Sub-streams for Streaming:** Use lower quality streams for better performance
6. **Document URLs:** Keep a list of your camera RTSP URLs for reference

---

## 🎯 Quick Reference

| Camera Type | URL Format | Example |
|------------|------------|---------|
| Webcam | Number (0, 1, 2...) | `0` |
| Hikvision | `rtsp://user:pass@ip:554/Streaming/Channels/101` | `rtsp://admin:12345@192.168.1.64:554/Streaming/Channels/101` |
| Dahua | `rtsp://user:pass@ip:554/cam/realmonitor?channel=1&subtype=0` | `rtsp://admin:admin@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0` |
| Generic IP | `rtsp://user:pass@ip:port/stream` | `rtsp://admin:password@192.168.1.100:554/stream1` |
| Video File | Absolute path | `C:\Videos\test.mp4` |

---

## 🆘 Still Having Issues?

1. **Check backend logs** for error messages
2. **Test camera manually** with `test_cctv.py`
3. **Verify MongoDB is running** (needed for camera data)
4. **Check browser console** (F12) for frontend errors
5. **Restart backend** and try again

---

## 📞 Next Steps After Adding Camera

1. ✅ Camera added successfully
2. ✅ Go to Dashboard
3. ✅ Click on your camera card
4. ✅ Click "Start Stream"
5. ✅ Adjust density threshold if needed (⚙️ settings icon)
6. ✅ Monitor crowd density in real-time!

---

**Happy Monitoring! 🎥📊**



