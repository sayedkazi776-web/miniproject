# 🔧 Fix Video Streaming Issue

## What I Fixed

1. **Socket.IO Connection URL**
   - Now uses `window.location.origin` when served from Flask
   - Automatically detects if running from Flask or Vite dev server

2. **Better Error Handling**
   - Added connection error handler
   - Better error messages
   - More logging for debugging

3. **Improved Backend Logging**
   - Shows when client connects
   - Shows when stream starts
   - Better error messages

## 🚀 Steps to Fix Your Video Issue

### Step 1: Rebuild Frontend (REQUIRED!)
Since we modified the frontend code, you need to rebuild:

```bash
cd frontend
npm run build
```

### Step 2: Restart Backend
```bash
cd backend
python app.py
```

### Step 3: Test Video
1. Open `http://localhost:5000`
2. Login/Register
3. Add a camera (use `0` for webcam)
4. Click camera → Start Stream
5. Check browser console (F12) for messages

## 🔍 Debugging Steps

### Check Browser Console (F12)
Look for:
- ✅ "✓ Socket.IO connected successfully"
- ✅ "✓ Video streamer ready"
- ✅ "Requesting stream for camera: [id]"

### Check Backend Console
Look for:
- ✅ "✓ Client connected to video streamer"
- ✅ "Received start_stream request for camera: [id]"
- ✅ "✓ Starting stream for camera: [id]"
- ✅ "Streaming started for camera [id] from [url]"

### Common Issues

1. **"Cannot connect to video server"**
   - Backend not running? Restart `python app.py`
   - Port 5000 in use? Check with `netstat -an | findstr 5000`

2. **"Could not open video source"**
   - Wrong camera index? Try `0`, `1`, `2`, etc.
   - Camera in use? Close other apps
   - No camera? Check if camera exists

3. **Socket connects but no video**
   - Check backend logs for errors
   - Try refreshing the page
   - Check if YOLO model loaded (backend console)

## 📝 Important Notes

- **MUST rebuild frontend** after code changes: `cd frontend && npm run build`
- **Browser console is your friend** - press F12 to see what's happening
- **Backend console shows** connection and stream status
- **Camera index**: Use `0` for first webcam, `1` for second, etc.

## ✅ What Should Happen

1. Click "Start Stream" button
2. Browser console: "Socket.IO connected"
3. Backend console: "Client connected"
4. Backend console: "Starting stream for camera..."
5. Backend console: "Streaming started..."
6. **Video appears in browser** 🎥

If video still doesn't work after rebuilding, check the error messages in both browser and backend consoles!

