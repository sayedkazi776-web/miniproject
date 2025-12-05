# JWT Authentication Fix

## Problem
Error: `module 'jwt' has no attribute 'encode'`

## Cause
The wrong JWT package was installed. There are two different JWT packages:
1. ❌ `jwt` (old package, version 1.4.0) - doesn't have `encode()` method
2. ✅ `PyJWT` (correct package, version 2.8.0) - has `encode()` and `decode()` methods

## Solution Applied
1. Uninstalled the wrong package: `pip uninstall jwt -y`
2. Installed the correct package: `pip install PyJWT==2.8.0`

## Verification
The authentication system now works correctly. You can:
- ✅ Login with: `admin@example.com` / `admin123`
- ✅ Register new users
- ✅ JWT tokens are generated and verified correctly

## How to Prevent This
Always install the correct package from `requirements.txt`:

```bash
cd backend
pip install -r requirements.txt
```

This ensures `PyJWT==2.8.0` is installed instead of the conflicting `jwt` package.

## If You Still Have Issues
1. **Restart the backend server** after installing PyJWT
2. Check that PyJWT is installed: `pip list | findstr jwt`
3. Verify it's the correct package: `python -c "import jwt; print(hasattr(jwt, 'encode'))"` should print `True`



