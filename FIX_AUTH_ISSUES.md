# Fix Authentication Issues

## Problem
- Cannot login with default email/password
- Cannot register new users

## Step 1: Check MongoDB Connection

First, make sure MongoDB is running:

**Windows:**
```bash
# Check if MongoDB service is running
net start MongoDB

# Or check Services (services.msc) for "MongoDB"
```

**Linux/Mac:**
```bash
# Start MongoDB
sudo systemctl start mongod

# Or check status
sudo systemctl status mongod
```

## Step 2: Run Diagnostic Tool

Test your database connection and authentication:

```bash
cd backend
python test_auth.py
```

This will:
- ✓ Test MongoDB connection
- ✓ Test user creation
- ✓ Check if admin user exists and password works

## Step 3: Initialize/Create Admin User

If admin user doesn't exist or password doesn't work, run:

```bash
# From project root
python db/init_db.py
```

This will create the admin user:
- **Email:** `admin@example.com`
- **Password:** `admin123`

## Step 4: Test Registration

If you want to register a new user, make sure:
1. MongoDB is running
2. Backend server is running (`python backend/app.py`)
3. Frontend is running (`cd frontend && npm run dev`)

Then try registering from the frontend.

## Common Issues

### Issue: "Database not initialized"
**Solution:** MongoDB is not running or connection URI is wrong
- Start MongoDB
- Check `MONGODB_URI` in `.env` file (if exists)
- Default is: `mongodb://127.0.0.1:27017/crowd_density_db`

### Issue: "Failed to create user"
**Solution:** 
- Check if MongoDB is connected
- Check if user already exists
- Look at backend console for error messages

### Issue: "Invalid credentials" on login
**Solution:**
- Run `python db/init_db.py` to recreate admin user
- Make sure you're using the correct email: `admin@example.com`
- Make sure you're using the correct password: `admin123`

## Quick Fix Commands

```bash
# 1. Test everything
cd backend
python test_auth.py

# 2. Create/reset admin user
python db/init_db.py

# 3. Start backend (in one terminal)
cd backend
python app.py

# 4. Start frontend (in another terminal)
cd frontend
npm run dev
```

## Still Having Issues?

1. **Check backend console** for error messages
2. **Check browser console** (F12) for frontend errors
3. **Run diagnostic tool:** `python backend/test_auth.py`
4. **Verify MongoDB is running** and accessible



