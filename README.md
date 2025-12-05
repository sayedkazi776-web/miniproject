# AI-based Crowd Density Monitoring for Event Safety

A comprehensive full-stack application for real-time crowd density monitoring using AI-powered person detection. The system processes video feeds from webcams or IP cameras, detects people using YOLOv8, calculates crowd density, and triggers alerts when thresholds are exceeded.

## 🎯 Features

- **User Authentication**: Secure JWT-based authentication system
- **Camera Management**: Add, manage, and monitor multiple camera feeds
- **Real-time AI Processing**: YOLOv8-powered person detection with bounding boxes
- **Crowd Density Calculation**: Automatic density calculation and visualization
- **Threshold-based Alerts**: Visual and real-time alerts when density exceeds safe limits
- **Historical Data Logging**: MongoDB-based logging for historical analysis
- **Modern UI**: Beautiful blue-themed responsive web interface built with React and Tailwind CSS
- **WebSocket Streaming**: Real-time video streaming and density updates

## 🏗️ Architecture

```
crowd-density-monitoring/
├── backend/                 # Python Flask backend
│   ├── app.py              # Main Flask application
│   ├── auth.py             # JWT authentication utilities
│   ├── models.py           # MongoDB database models
│   ├── routes/             # API route handlers
│   │   ├── user_routes.py
│   │   ├── camera_routes.py
│   │   └── monitoring_routes.py
│   ├── ai_processor/       # AI/CV processing modules
│   │   ├── yolo_model.py   # YOLOv8 person detection
│   │   ├── density_detector.py  # Density calculation
│   │   └── video_streamer.py    # Video streaming handler
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── pages/          # Page components
│   │   ├── components/     # Reusable components
│   │   ├── context/        # React context (Auth)
│   │   └── services/       # API services
│   └── package.json
└── README.md
```

## 📋 Prerequisites

### Backend Requirements
- Python 3.9 or higher
- MongoDB (local installation or MongoDB Atlas account)
- Webcam or IP camera with RTSP support (optional, can use webcam index)

### Frontend Requirements
- Node.js 16+ and npm/yarn

## 🚀 Quick Start - Run Everything from app.py!

### Prerequisites
- Python 3.9+ installed
- MongoDB running locally or MongoDB Atlas account
- Node.js 16+ and npm (for building frontend)

### ⭐ EASIEST WAY: Run Everything from One File!

```bash
# Option 1: Use the build script (recommended)
# Just double-click: build_and_run.bat

# Option 2: Manual steps
cd frontend
npm install          # First time only
npm run build       # Build the frontend

cd ../backend
python app.py       # Run everything - frontend + backend!
```

**That's it!** Open `http://localhost:5000` in your browser - both frontend and backend run from one server!

### Alternative: Development Mode (Two Servers)

If you prefer to run frontend and backend separately during development:

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Then access `http://localhost:3000` (frontend dev server proxies to backend on port 5000)

### 3. Initialize Database (Optional)

To create a sample admin user and camera:

```bash
# From project root
python db/init_db.py
```

This creates:
- Admin user: `admin@example.com` / `admin123`
- Sample camera using webcam index 0

## 🔧 Configuration

### 📹 Adding Cameras

**Quick Start - Add Your Webcam:**
```bash
# Make sure backend is running first
cd backend
python app.py

# In a new terminal, run:
python add_webcam.py
```

**📖 Complete Guide:** See [CCTV_CAMERA_GUIDE.md](CCTV_CAMERA_GUIDE.md) for detailed instructions on adding:
- Webcams (USB/Integrated)
- IP Cameras (RTSP)
- CCTV Cameras
- Video files (for testing)

### Camera Configuration

When adding a camera, you can use:

1. **Webcam Index**: Use `0`, `1`, `2`, etc. for local webcams
   - `0` = First webcam
   - `1` = Second webcam
   - etc.

2. **RTSP URL**: For IP cameras, use RTSP URLs:
   - Example: `rtsp://username:password@camera-ip:554/stream`

3. **File Path**: For testing with video files:
   - Example: `/path/to/video.mp4`

### Density Threshold Configuration

The default density threshold is `0.65` (65% normalized density). You can adjust this:
- **Low**: 0.3-0.5 (fewer alerts)
- **Medium**: 0.5-0.7 (balanced)
- **High**: 0.7-0.9 (more sensitive)

## 📱 Usage

### 1. Register/Login
- Navigate to `http://localhost:3000`
- Register a new account or login with existing credentials

### 2. Add Camera
- Click "Add Camera" on the dashboard
- Enter camera name, URL/index, and location
- Click "Add Camera"

### 3. Start Monitoring
- Click on a camera card from the dashboard
- Click "Start Stream" to begin monitoring
- View real-time person detection and density metrics

### 4. Configure Alerts
- Click the settings icon (⚙️) on the monitoring page
- Adjust the density threshold slider
- Alerts will trigger when density exceeds the threshold

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Cameras
- `GET /api/cameras` - List all cameras
- `POST /api/cameras` - Create new camera
- `GET /api/cameras/:id` - Get camera details
- `PUT /api/cameras/:id` - Update camera
- `DELETE /api/cameras/:id` - Delete camera

### Monitoring
- `GET /api/monitoring/density/:camera_id` - Get density history
- `POST /api/monitoring/start/:camera_id` - Start monitoring
- `POST /api/monitoring/stop/:camera_id` - Stop monitoring

### WebSocket Events
- `start_stream` - Start video stream for a camera
- `stop_stream` - Stop video stream
- `frame` - Receive video frame and density data
- `error` - Receive error messages

## 🗄️ Database Schema

### Users Collection
```javascript
{
  _id: ObjectId,
  email: String (unique, indexed),
  password_hash: String,
  name: String,
  created_at: Date
}
```

### Cameras Collection
```javascript
{
  _id: ObjectId,
  name: String (unique),
  url: String,
  location: String,
  owner_id: ObjectId,
  created_at: Date
}
```

### Density Logs Collection
```javascript
{
  _id: ObjectId,
  camera_id: ObjectId,
  timestamp: Date,
  person_count: Integer,
  density_value: Float,
  alert_triggered: Boolean
}
```

## 🐛 Troubleshooting

### Backend Issues

**Issue**: YOLOv8 model not loading
- **Solution**: Ensure `ultralytics` is installed: `pip install ultralytics`
- The model will auto-download on first use (~6MB)

**Issue**: MongoDB connection error
- **Solution**: Verify MongoDB is running and `MONGODB_URI` in `.env` is correct
- For MongoDB Atlas, ensure your IP is whitelisted

**Issue**: WebSocket connection failed
- **Solution**: Ensure Flask-SocketIO and eventlet are installed
- Check firewall settings for port 5000

### Frontend Issues

**Issue**: Cannot connect to backend
- **Solution**: Verify backend is running on port 5000
- Check `vite.config.js` proxy settings

**Issue**: Video not displaying
- **Solution**: Check browser console for errors
- Verify camera URL/index is correct
- Ensure WebSocket connection is established

### Camera Issues

**Issue**: Webcam not working
- **Solution**: Try different webcam indices (0, 1, 2...)
- Check camera permissions on your system
- On Linux, ensure user is in `video` group

**Issue**: RTSP stream not connecting
- **Solution**: Verify RTSP URL format is correct
- Check network connectivity to camera
- Ensure camera credentials are correct

## 🔒 Security Considerations

1. **Change Default Secrets**: Always change `SECRET_KEY` and `JWT_SECRET_KEY` in production
2. **Use HTTPS**: Deploy with HTTPS in production environments
3. **MongoDB Security**: Enable authentication for MongoDB in production
4. **API Rate Limiting**: Consider adding rate limiting for production use
5. **Input Validation**: Additional input validation may be needed for production

## 🚢 Deployment

### Backend Deployment
1. Set `FLASK_DEBUG=False` in production
2. Use a production WSGI server (e.g., Gunicorn with eventlet workers)
3. Configure MongoDB Atlas for cloud database
4. Set up environment variables securely

### Frontend Deployment
1. Build production bundle: `npm run build`
2. Serve `dist/` folder with a web server (nginx, Apache, etc.)
3. Configure API proxy in web server

## 📊 Performance Notes

- YOLOv8n (nano) model is used for faster inference
- Frame rate is limited to ~10 FPS to reduce CPU load
- For higher performance, consider using GPU acceleration
- Density logging occurs every 5 seconds to reduce database writes

## 🤝 Contributing

This is a complete implementation ready for use. To extend:

1. Add camera calibration for accurate density calculation
2. Implement user roles and permissions
3. Add email/SMS notifications for alerts
4. Implement advanced analytics and reporting
5. Add support for multiple simultaneous streams per user

## 📝 License

This project is provided as-is for educational and commercial use.

## 🙏 Acknowledgments

- YOLOv8 by Ultralytics
- Flask and Flask-SocketIO communities
- React and Tailwind CSS communities

---

**Note**: For production deployment, ensure all security best practices are followed, including proper secret management, HTTPS, and database security.

