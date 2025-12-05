# 📹 How to Add Your Camera

## Method 1: Using the Web Interface (Easiest)

1. **Start the application:**
   ```bash
   cd backend
   python app.py
   ```
   Then open: `http://localhost:5000`

2. **Login** with your account

3. **Go to Dashboard** (you should see it automatically)

4. **Click "Add Camera" button** (blue button at top right)

5. **Fill in the form:**
   - **Camera Name**: `My Webcam`
   - **Video URL / Webcam Index**: `0`
   - **Location**: `Main Entrance`

6. **Click "Add Camera"**

7. **Done!** You should see your camera card appear

## Method 2: Using the Script (Alternative)

1. **Make sure backend is running:**
   ```bash
   cd backend
   python app.py
   ```

2. **In a NEW terminal, run:**
   ```bash
   python add_camera.py
   ```

3. **Enter your email and password** when prompted

4. **Camera will be added automatically!**

## 📝 Camera URL Options

### For Webcam:
- `0` - First webcam (most common)
- `1` - Second webcam
- `2` - Third webcam
- etc.

### For IP Camera:
- `rtsp://username:password@192.168.1.100:554/stream`

### For Video File:
- `/path/to/video.mp4` (absolute path)
- `C:\Videos\test.mp4` (Windows)

## ✅ After Adding Camera

1. **Click on the camera card** from Dashboard
2. **Click "Start Stream"** button
3. **Video should appear!** 🎥

## 🔍 Troubleshooting

**"Invalid camera URL" error?**
- Make sure URL is a number (0, 1, 2...) for webcam
- No spaces or letters

**"Could not open video source" error?**
- Try different index: 0, 1, 2, etc.
- Check camera permissions (Windows Settings → Privacy → Camera)
- Make sure no other app is using the camera

**"Camera name already exists"?**
- Use a different name
- Or delete the old camera first

