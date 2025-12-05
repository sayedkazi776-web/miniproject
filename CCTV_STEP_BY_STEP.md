# 🎯 Step-by-Step: Adding Your CCTV Camera

## ✅ Good News: Your System Already Supports CCTV!

Your crowd density monitoring system **already works with CCTV cameras**! No code changes needed. Just follow these steps.

---

## 🎬 Step 1: Get Your Camera Information

You need these 4 pieces of information:

| What | Where to Find | Example |
|------|--------------|---------|
| **IP Address** | Router admin panel / camera settings | `192.168.1.100` |
| **Username** | Camera web interface | `admin` |
| **Password** | Camera setup / default credentials | `password123` |
| **Stream Path** | Camera manual / web interface | `stream1` or `/Streaming/Channels/101` |

### How to Access Your Camera:

1. **Find Camera IP:**
   ```powershell
   # In PowerShell:
   arp -a | Select-String "dynamic"
   ```
   Or check your router's connected devices list

2. **Open Camera Web Interface:**
   - Open browser: `http://YOUR_CAMERA_IP`
   - Login with username/password
   - Look for "RTSP Settings" or "Streaming"

---

## 🧪 Step 2: Test Your RTSP URL (CRITICAL!)

**You MUST test before adding!**

### Option A: Quick Test with Python

```bash
python test_cctv.py
```

Enter your RTSP URL when prompted. If video shows up, you're ready!

### Option B: Test with VLC Media Player

1. **Download VLC:** https://www.videolan.org/vlc/
2. **Open VLC**
3. **Media → Open Network Stream** (or `Ctrl+N`)
4. **Enter RTSP URL**
5. **Click Play**

**If video appears** → ✅ Success! You can add it to the system.  
**If error appears** → ❌ Fix the URL first.

### Example RTSP URLs to Try:

```bash
# Hikvision cameras:
rtsp://admin:password@192.168.1.64:554/Streaming/Channels/101

# Dahua cameras:
rtsp://admin:password@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0

# Generic IP camera:
rtsp://admin:password@192.168.1.100:554/stream1

# Axis cameras:
rtsp://root:password@192.168.1.10/axis-media/media.amp
```

---

## ➕ Step 3: Add Camera to Your System

### **Method A: Web Interface (EASIEST)**

1. **Start the backend server:**
   ```bash
   cd backend
   python app.py
   ```
   Wait until you see: `✓ Backend API server starting on http://localhost:5000`

2. **Open browser and go to:**
   ```
   http://localhost:5000
   ```

3. **Login** with your email and password

4. **Click "Add Camera"** button (usually at top right)

5. **Fill in the form:**
   ```
   Camera Name:  Front Door CCTV
   URL:          rtsp://admin:password123@192.168.1.100:554/stream1
   Location:     Main Entrance
   ```

6. **Click "Add Camera"** button

7. **Success!** ✅ Your camera appears on the dashboard

### **Method B: Using the Script**

1. **Edit `add_camera.py`:**
   ```python
   CAMERA_NAME = "My CCTV Camera"
   CAMERA_URL = "rtsp://admin:password123@192.168.1.100:554/stream1"
   CAMERA_LOCATION = "Front Entrance"
   ```

2. **Make sure backend is running:**
   ```bash
   cd backend
   python app.py
   ```

3. **In a NEW terminal, run:**
   ```bash
   python add_camera.py
   ```

4. **Enter your email and password**

5. **Camera added!** ✅

---

## 🎥 Step 4: Start Monitoring

1. **Go to Dashboard** (you should already be there)

2. **Find your CCTV camera card**

3. **Click on the camera card**

4. **Click "Start Stream" button**

5. **Wait 5-10 seconds** for connection

6. **Video should appear!** 🎉

**What you should see:**
- ✅ Live video feed from your CCTV
- ✅ Green boxes around detected people
- ✅ People count at top left
- ✅ Density percentage
- ✅ Alerts if crowd is too dense

---

## 🔧 Troubleshooting: Camera Not Working?

### Issue: "Could not open video source"

**FIX:**
1. Test RTSP URL in VLC first (MUST work there!)
2. Check username/password
3. Verify camera IP address
4. Try different stream paths
5. Ensure camera is powered on and connected

### Issue: "Connection timeout"

**FIX:**
1. Check network connection
2. Ping camera: `ping 192.168.1.100`
3. Check firewall settings
4. Verify RTSP port (usually 554)

### Issue: "Authentication failed"

**FIX:**
1. Double-check username and password
2. Try default credentials
3. Reset camera if needed

### Issue: Video freezes or is laggy

**FIX:**
1. Use sub-stream (lower quality)
2. Reduce camera resolution
3. Check network bandwidth
4. Use wired Ethernet

### Issue: Stream disconnects after a while

**FIX:**
1. Restart backend server
2. Check camera has no timeout settings
3. Update camera firmware

---

## 📋 Common CCTV Brands and RTSP URLs

### **Hikvision:**
```
rtsp://username:password@192.168.1.64:554/Streaming/Channels/101
rtsp://username:password@192.168.1.64:554/Streaming/Channels/102  (sub-stream)
```

### **Dahua:**
```
rtsp://admin:password@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0
rtsp://admin:password@192.168.1.108:554/cam/realmonitor?channel=1&subtype=1  (sub)
```

### **Axis:**
```
rtsp://username:password@192.168.1.10/axis-media/media.amp
rtsp://username:password@192.168.1.10/mpeg4/media.amp
```

### **Uniview:**
```
rtsp://admin:password@192.168.1.100:554/Streaming/Channels/101
```

### **Reolink:**
```
rtsp://admin:password@192.168.1.10:554/h264Preview_01_main
rtsp://admin:password@192.168.1.10:554/h264Preview_01_sub  (sub)
```

### **Generic/Unbranded:**
Try these patterns:
```
rtsp://admin:password@192.168.1.100:554/stream1
rtsp://admin:password@192.168.1.100:554/h264
rtsp://admin:password@192.168.1.100:554/live
rtsp://admin:password@192.168.1.100:554/video
```

---

## ✅ Checklist: Before Adding CCTV

- [ ] Camera is powered on
- [ ] Camera is connected to network
- [ ] I know the camera IP address
- [ ] I know the username and password
- [ ] I tested the RTSP URL in VLC Media Player
- [ ] Video worked in VLC test
- [ ] Backend server is running
- [ ] I'm logged into the web interface

---

## 🎯 Quick Reference Commands

```bash
# Start backend
cd backend
python app.py

# Test CCTV camera
python test_cctv.py

# Add camera via script
python add_camera.py

# View database
cd backend
python view_database.py

# Check if camera works (from backend folder)
python -c "import cv2; cap = cv2.VideoCapture('rtsp://admin:password@192.168.1.100:554/stream1'); print('Works!' if cap.isOpened() else 'Failed')"
```

---

## 📚 More Help

| Topic | File |
|-------|------|
| Detailed CCTV guide | `CCTV_CAMERA_SETUP.md` |
| Quick reference | `QUICK_ADD_CCTV.txt` |
| Camera setup guide | `CAMERA_SETUP.md` |
| How to add camera | `ADD_CAMERA_GUIDE.md` |
| Troubleshooting | See guide files above |

---

## 💡 Pro Tips

1. **Always test in VLC first** - If it doesn't work there, it won't work in the system
2. **Use wired connection** - More stable than WiFi
3. **Start with lower quality** - Sub-streams are more reliable for streaming
4. **Check firewall** - Make sure RTSP port (554) is open
5. **One camera at a time** - Add and test one before adding more
6. **Check logs** - Look at backend console for error messages

---

## 🎉 You're Done!

If you followed all steps and tested in VLC:
- ✅ Your CCTV camera should be working
- ✅ You should see live video feed
- ✅ Person detection should be working
- ✅ Density calculations should appear
- ✅ Alerts should trigger when crowded

**Enjoy your crowd density monitoring system!** 🎥📊

---

**Need help?** Check the troubleshooting section or look at the detailed guides in this folder.


