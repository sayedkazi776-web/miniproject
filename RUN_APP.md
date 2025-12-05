# 🚀 Run the Complete Project from app.py

## ✅ Everything Runs from One File!

You can now run the **entire application** (frontend + backend) just by running `app.py`!

## Quick Start (2 Steps)

### Step 1: Build the Frontend (First Time Only)
```bash
cd frontend
npm install
npm run build
```

### Step 2: Run Everything
```bash
cd backend
python app.py
```

**That's it!** Open `http://localhost:5000` in your browser!

## Or Use the Build Script

**Just double-click:** `build_and_run.bat`

This will:
1. Build the frontend automatically
2. Start the server
3. Everything runs from one command!

## How It Works

- Flask (`app.py`) serves the React frontend from the `frontend/dist` folder
- All API routes work normally at `/api/...`
- All frontend routes are handled by React Router
- One server, one port (5000), everything works!

## Access the Application

🌐 **Open:** `http://localhost:5000`

- Frontend: Served from Flask
- Backend API: Available at `/api/...`
- WebSocket: Available at `/socket.io`

## Rebuilding Frontend

If you change the frontend code:

```bash
cd frontend
npm run build
```

Then restart `app.py` - no need to run two servers!

---

**Note:** For development with hot-reload, you can still run frontend separately:
```bash
cd frontend
npm run dev  # Access at http://localhost:3000
```

But for production or simple usage, just build once and run `app.py`!

