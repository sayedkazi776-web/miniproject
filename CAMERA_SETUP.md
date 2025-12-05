# Camera Setup and Access Guide

This guide explains how to configure and access cameras for the Crowd Density Monitoring system.

## Camera Types Supported

1. **Local Webcams** (USB/Integrated)
2. **IP Cameras** (RTSP streams)
3. **Video Files** (for testing)

## Method 1: Local Webcam Access

### Finding Your Webcam Index

**Windows:**
```powershell
# List available video devices
Get-CimInstance Win32_PnPEntity | Where-Object {$_.Name -like "*camera*" -or $_.Name -like "*webcam*"}
```

**Linux:**
```bash
# List video devices
ls -l /dev/video*
# Usually: /dev/video0, /dev/video1, etc.
```

**Mac:**
```bash
# List video devices
system_profiler SPCameraDataType
```

### Common Webcam Indices

- `0` - First/default webcam
- `1` - Second webcam (if available)
- `2` - Third webcam (if available)
- etc.

### Adding Webcam to System

1. **Login** to the application
2. **Go to Dashboard**
3. **Click "Add Camera"**
4. **Enter Details**:
   - **Name**: "My Webcam" or any name
   - **URL**: `0` (for first webcam) or `1`, `2`, etc.
   - **Location**: "Main Entrance" or any location
5. **Click "Add Camera"**

### Testing Webcam Access

**Python Test Script** (`test_webcam.py`):
```python
import cv2

# Test webcam index 0
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open webcam 0")
else:
    print("Webcam 0 is accessible")
    ret, frame = cap.read()
    if ret:
        print("Successfully read frame")
        print(f"Frame size: {frame.shape}")
    cap.release()
```

Run: `python test_webcam.py`

## Method 2: IP Camera Access (RTSP)

### Finding RTSP URL

Most IP cameras use RTSP (Real-Time Streaming Protocol). Common formats:

```
rtsp://username:password@camera-ip:port/stream-path
```

### Common RTSP URLs by Brand

**Hikvision:**
```
rtsp://admin:password@192.168.1.64:554/Streaming/Channels/101
```

**Dahua:**
```
rtsp://admin:password@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0
```

**Axis:**
```
rtsp://username:password@192.168.1.10/axis-media/media.amp
```

**Generic:**
```
rtsp://username:password@camera-ip:554/stream1
rtsp://username:password@camera-ip:554/h264
rtsp://username:password@camera-ip:554/live
```

### Finding Your Camera's IP Address

1. **Check Router Admin Panel**: Most routers show connected devices
2. **Use Network Scanner**: Tools like Advanced IP Scanner, Angry IP Scanner
3. **Check Camera Settings**: Access camera web interface (usually port 80)

### Testing RTSP Stream

**Using VLC Media Player:**
1. Open VLC
2. Media → Open Network Stream
3. Enter RTSP URL
4. Click Play

**Using FFmpeg:**
```bash
ffmpeg -rtsp_transport tcp -i "rtsp://username:password@ip:port/stream" -vcodec copy -acodec copy test.mp4
```

**Python Test Script** (`test_rtsp.py`):
```python
import cv2

rtsp_url = "rtsp://username:password@192.168.1.64:554/stream"
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print(f"Cannot open RTSP stream: {rtsp_url}")
else:
    print("RTSP stream is accessible")
    ret, frame = cap.read()
    if ret:
        print("Successfully read frame")
    cap.release()
```

### Adding IP Camera to System

1. **Login** to the application
2. **Go to Dashboard**
3. **Click "Add Camera"**
4. **Enter Details**:
   - **Name**: "Front Entrance Camera"
   - **URL**: `rtsp://username:password@192.168.1.64:554/stream`
   - **Location**: "Front Entrance"
5. **Click "Add Camera"**

### Troubleshooting RTSP

**Issue: Connection timeout**
- Check camera IP address is correct
- Verify network connectivity: `ping camera-ip`
- Check firewall settings
- Verify RTSP port (usually 554)

**Issue: Authentication failed**
- Verify username/password
- Check camera supports RTSP
- Try accessing camera web interface first

**Issue: Stream not loading**
- Some cameras require TCP transport: Add `?tcp=1` to URL
- Try different stream paths (stream1, stream2, etc.)
- Check camera codec compatibility (H.264 recommended)

## Method 3: Video File Access (Testing)

For testing without a camera, you can use video files:

1. **Add Camera** with:
   - **Name**: "Test Video"
   - **URL**: `/path/to/video.mp4` (absolute path)
   - **Location**: "Testing"

**Supported Formats:**
- `.mp4`
- `.avi`
- `.mov`
- `.mkv`
- Any format supported by OpenCV

## Camera Permissions

### Windows
- Grant camera access in Windows Settings → Privacy → Camera
- Run application as Administrator if needed

### Linux
- Add user to `video` group:
  ```bash
  sudo usermod -a -G video $USER
  ```
- Logout and login again

### Mac
- Grant camera permissions in System Preferences → Security & Privacy → Camera

## Multiple Camera Setup

You can add multiple cameras:

1. **Webcam 1**: URL = `0`
2. **Webcam 2**: URL = `1`
3. **IP Camera**: URL = `rtsp://...`
4. **Another IP Camera**: URL = `rtsp://...`

Each camera can be monitored independently on the dashboard.

## Camera Configuration Tips

### For Best Performance:
- Use **H.264** codec (most compatible)
- Set resolution to **720p or 1080p** (not higher)
- Use **TCP transport** for RTSP (more reliable)
- Ensure stable network connection

### For Testing:
- Start with webcam index `0`
- Use a test video file
- Test RTSP with VLC first before adding to system

## Monitoring Camera Status

In the application:
1. **Dashboard**: Shows all cameras
2. **Monitoring Page**: Shows camera status (Active/Inactive)
3. **Error Messages**: Display if camera cannot be accessed

## Common Issues and Solutions

**"Cannot open video source"**
- Check camera URL/index is correct
- Verify camera is not being used by another application
- Restart camera or computer

**"Stream disconnected"**
- Check network connection (for IP cameras)
- Verify camera is powered on
- Check RTSP credentials

**"Low frame rate"**
- Reduce camera resolution
- Check network bandwidth (for IP cameras)
- Close other applications using camera

**"No video feed"**
- Test camera in another application (e.g., VLC)
- Check camera permissions
- Try different camera index

## Testing Your Setup

1. **Add camera** using one of the methods above
2. **Click on camera** from dashboard
3. **Click "Start Stream"**
4. **Verify** video feed appears
5. **Check** person detection and density calculation works

## Advanced: Custom Camera Sources

You can also use:
- **HTTP MJPEG streams**: `http://camera-ip/video.mjpg`
- **USB device paths**: `/dev/video0` (Linux)
- **Screen capture**: Using tools like OBS Virtual Camera

For custom sources, ensure they're compatible with OpenCV's `VideoCapture`.

