# 🚀 Complete Setup Guide - Get Everything Running

## Step 1: Install Prerequisites

### Backend Requirements
```bash
# Python 3.9+ (check with: python --version)
# MongoDB (local or Atlas)

# Install Python dependencies
cd backend
pip install -r requirements.txt
```

### Frontend Requirements
```bash
# Node.js 16+ (check with: node --version)
# npm comes with Node.js

# Install frontend dependencies
cd frontend
npm install
```

## Step 2: Start MongoDB

**Windows:**
- Start MongoDB service from Services
- Or run: `net start MongoDB`

**Linux:**
```bash
sudo systemctl start mongod
```

**Mac:**
```bash
brew services start mongodb-community
```

Or use **MongoDB Atlas** (cloud) - no installation needed!

## Step 3: Run the Project

### Option A: Use the Easy Scripts (Recommended)

**Double-click:** `start_all.bat`

This will:
- Start backend on port 5000
- Start frontend on port 3000
- Open both in separate windows

### Option B: Manual Start (Two Terminals)

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Step 4: Access the Application

🌐 **Open your browser and go to:** `http://localhost:3000`

## Step 5: Create Your First Account

1. Click "Sign up" on the login page
2. Enter your email, password, and name
3. You'll be logged in automatically

## Step 6: Add a Camera

1. Click "Add Camera" button
2. Enter:
   - **Name**: "My Webcam"
   - **URL**: `0` (for first webcam) or `1`, `2`, etc.
   - **Location**: "Main Entrance"
3. Click "Add Camera"

## Step 7: Start Monitoring

1. Click on your camera card
2. Click "Start Stream" button
3. Watch real-time crowd detection!

## 🎯 Quick Test Checklist

- [ ] Backend running? → Check `http://localhost:5000/api/health`
- [ ] Frontend running? → Check `http://localhost:3000`
- [ ] MongoDB running? → Backend should connect without errors
- [ ] Can register/login? → Create account on frontend
- [ ] Can add camera? → Add a camera from dashboard
- [ ] Can view stream? → Click camera and start stream

## 🔧 Troubleshooting

### Backend won't start?
- Check MongoDB is running
- Check port 5000 is free
- Install dependencies: `pip install -r backend/requirements.txt`

### Frontend won't start?
- Install dependencies: `npm install` in frontend folder
- Check port 3000 is free
- Check Node.js is installed

### "Cannot connect to backend"?
- Make sure backend is running on port 5000
- Check `http://localhost:5000/api/health` in browser

### Camera not working?
- Try different webcam index (0, 1, 2...)
- Check camera permissions
- For IP cameras, verify RTSP URL is correct

## 📝 Notes

- Backend API: `http://localhost:5000` (API only, don't access directly)
- Frontend App: `http://localhost:3000` (USE THIS!)
- Database: MongoDB (local or Atlas)
- Webcam: Use index `0` for first webcam, `1` for second, etc.

---
**You're all set!** The project is ready to use. 🎉

