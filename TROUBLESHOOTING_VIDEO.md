# Video Streaming Troubleshooting Guide

## Issue: Video Not Opening / Not Streaming

### Quick Checks

1. **Check Browser Console**
   - Press F12 → Console tab
   - Look for errors (red text)
   - Should see "Socket.IO connected successfully"

2. **Check Backend Console**
   - Should see "✓ Client connected to video streamer"
   - Should see "✓ Starting stream for camera: [id]"
   - Should see "Streaming started for camera [id] from [url]"

### Common Issues & Solutions

#### 1. Socket.IO Not Connecting

**Symptoms:**
- Console shows "Cannot connect to video server"
- No "Socket connected" message

**Solutions:**
- Make sure backend is running (`python app.py`)
- Check if port 5000 is accessible
- Try refreshing the page
- Check browser console for connection errors

#### 2. Camera Not Opening

**Symptoms:**
- Socket connects but no video appears
- Backend shows "Could not open video source"

**Solutions:**

**For Webcam:**
- Try different webcam indices: `0`, `1`, `2`, etc.
- Check camera permissions:
  - Windows: Settings → Privacy → Camera
  - Mac: System Preferences → Security → Camera
  - Linux: Check video group membership
- Close other apps using the camera

**For IP Camera (RTSP):**
- Verify RTSP URL format: `rtsp://username:password@ip:port/stream`
- Test URL in VLC media player first
- Check network connectivity
- Verify camera credentials

#### 3. Stream Starts But No Frames

**Symptoms:**
- Socket connected, stream started, but black screen

**Solutions:**
- Check browser console for frame errors
- Verify YOLO model loaded (check backend console)
- Try restarting the stream
- Check if camera is actually capturing (test in another app)

#### 4. YOLO Model Not Loading

**Symptoms:**
- Backend shows "Warning: Could not load YOLO model"

**Solutions:**
```bash
cd backend
pip install ultralytics
# Model will auto-download on first use
```

### Debug Steps

1. **Enable Console Logging:**
   - Open browser DevTools (F12)
   - Go to Console tab
   - Look for Socket.IO messages

2. **Check Network Tab:**
   - DevTools → Network tab
   - Filter by "WS" (WebSocket)
   - Should see connection to `/socket.io/`

3. **Test Camera Manually:**
   ```python
   # Test in Python
   import cv2
   cap = cv2.VideoCapture(0)  # Use your camera index
   ret, frame = cap.read()
   print(f"Camera opened: {ret}")
   cap.release()
   ```

4. **Verify Camera in Dashboard:**
   - Go to Dashboard
   - Check camera URL is correct
   - Try editing camera and updating URL

### Browser-Specific Issues

**Chrome/Edge:**
- Check camera permissions
- Allow insecure content if using HTTP

**Firefox:**
- May need explicit permission
- Check about:permissions

**Safari:**
- May require HTTPS for camera access

### Still Not Working?

1. Check backend logs for errors
2. Try a different camera/index
3. Test with a simple video file path instead
4. Verify MongoDB is running (needed for camera data)
5. Restart both backend and browser

