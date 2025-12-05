# Quick Start Guide

## ⚠️ Important: You Need TWO Terminals Running!

This project has a **backend** (Flask API) and a **frontend** (React app). You must run both.

### Terminal 1: Backend (Python Flask API)
python app.py
```
✅ Backend runs on: `http://localhost:5000`

### Terminal 2: Frontend (React App)
```bash
cd frontend
npm install   # Only needed the first time
npm run dev
```
✅ Frontend runs on: `http://localhost:3000`

## 🎯 Access the Application

**Open your browser and go to:** `http://localhost:3000`

**DO NOT** access `http://localhost:5000` directly - that's only the API server and will show "Not Found" errors for non-API routes.

## 🔍 Troubleshooting

### "Not Found" Error?
- Make sure you're accessing `http://localhost:3000` (frontend), not `http://localhost:5000` (backend API)
- Make sure both backend and frontend are running
- Check the terminal outputs for errors

### Backend Not Starting?
- Make sure MongoDB is running
- Check if port 5000 is already in use
- Verify Python dependencies: `pip install -r backend/requirements.txt`

### Frontend Not Starting?
- Make sure Node.js is installed
- Install dependencies: `npm install` in the frontend directory
- Check if port 3000 is already in use

