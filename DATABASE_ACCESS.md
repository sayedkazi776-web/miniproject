# Database Access Guide

This guide explains how to access and view your MongoDB database output for the Crowd Density Monitoring system.

## Database Information

- **Database Name**: `crowd_density_db` (or as specified in MONGODB_URI)
- **Collections**:
  - `users` - User accounts
  - `cameras` - Camera configurations
  - `density_logs` - Historical density data

## Method 1: MongoDB Shell (mongosh)

### View All Collections
```bash
mongosh
use crowd_density_db
show collections
```

### View Users
```bash
db.users.find().pretty()
```

### View Cameras
```bash
db.cameras.find().pretty()
```

### View Density Logs
```bash
# All logs
db.density_logs.find().pretty()

# Recent logs (last 10)
db.density_logs.find().sort({timestamp: -1}).limit(10).pretty()

# Logs for specific camera
db.density_logs.find({camera_id: ObjectId("YOUR_CAMERA_ID")}).sort({timestamp: -1}).pretty()

# Logs with alerts
db.density_logs.find({alert_triggered: true}).sort({timestamp: -1}).pretty()

# Count total logs
db.density_logs.countDocuments()
```

### Advanced Queries

```bash
# Get density statistics for a camera
db.density_logs.aggregate([
  { $match: { camera_id: ObjectId("YOUR_CAMERA_ID") } },
  { $group: {
      _id: null,
      avgDensity: { $avg: "$density_value" },
      maxDensity: { $max: "$density_value" },
      minDensity: { $min: "$density_value" },
      avgPersonCount: { $avg: "$person_count" },
      totalAlerts: { $sum: { $cond: ["$alert_triggered", 1, 0] } }
    }
  }
])

# Get logs from last hour
db.density_logs.find({
  timestamp: { $gte: new Date(Date.now() - 3600000) }
}).sort({timestamp: -1}).pretty()

# Export data to JSON
mongoexport --db=crowd_density_db --collection=density_logs --out=density_logs.json --pretty
```

## Method 2: MongoDB Compass (GUI Tool)

### Installation
1. Download from: https://www.mongodb.com/try/download/compass
2. Install and open MongoDB Compass
3. Connect using your connection string:
   - Local: `mongodb://127.0.0.1:27017`
   - Atlas: Your MongoDB Atlas connection string

### Using Compass
1. **Connect**: Enter connection string and click "Connect"
2. **Select Database**: Click on `crowd_density_db`
3. **Browse Collections**: Click on any collection to view data
4. **Filter & Sort**: Use the filter bar to query data
5. **Export**: Right-click collection → Export Collection

## Method 3: Python Script (Included)

Create a file `view_database.py` in the backend directory:

```python
from models import init_db, User, Camera, DensityLog
from dotenv import load_dotenv
import os
from bson import ObjectId

load_dotenv()
init_db(os.getenv('MONGODB_URI', 'mongodb://127.0.0.1:27017/crowd_density_db'))

print("=== USERS ===")
users = User.find_all() if hasattr(User, 'find_all') else []
for user in users:
    print(f"ID: {user['_id']}, Email: {user['email']}, Name: {user.get('name', 'N/A')}")

print("\n=== CAMERAS ===")
cameras = Camera.find_all()
for cam in cameras:
    print(f"ID: {cam['_id']}, Name: {cam['name']}, Location: {cam.get('location', 'N/A')}, URL: {cam['url']}")

print("\n=== DENSITY LOGS (Last 10) ===")
# Get logs from all cameras (approximate)
from models import db
logs = list(db.db.density_logs.find().sort('timestamp', -1).limit(10))
for log in logs:
    print(f"Camera: {log['camera_id']}, Time: {log['timestamp']}, People: {log['person_count']}, Density: {log['density_value']}, Alert: {log.get('alert_triggered', False)}")
```

Run it:
```bash
cd backend
python view_database.py
```

## Method 4: API Endpoints

You can also access data via the API:

```bash
# Get cameras (requires auth token)
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:5000/api/cameras

# Get density history (requires auth token)
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:5000/api/monitoring/density/CAMERA_ID
```

## Database Location

### Local MongoDB
- **Windows**: Usually `C:\data\db\` or configured in `mongod.cfg`
- **Linux**: `/var/lib/mongodb/`
- **Mac**: `/usr/local/var/mongodb/`

### MongoDB Atlas (Cloud)
- Access via MongoDB Compass or mongosh using connection string
- Data is stored in the cloud

## Useful Database Commands

### Clear All Data (CAUTION!)
```bash
mongosh
use crowd_density_db
db.users.deleteMany({})
db.cameras.deleteMany({})
db.density_logs.deleteMany({})
```

### Backup Database
```bash
mongodump --db=crowd_density_db --out=./backup
```

### Restore Database
```bash
mongorestore --db=crowd_density_db ./backup/crowd_density_db
```

## Monitoring Database Size

```bash
mongosh
use crowd_density_db
db.stats()
```

## Real-time Monitoring

For real-time database monitoring, you can use:

1. **MongoDB Compass**: Shows real-time data as it's inserted
2. **MongoDB Atlas**: Built-in monitoring dashboard
3. **Custom Script**: Run a watch query:

```javascript
// In mongosh
use crowd_density_db
db.density_logs.watch().forEach(change => printjson(change))
```

