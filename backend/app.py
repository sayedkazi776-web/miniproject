"""
Main Flask application for AI-based Crowd Density Monitoring System
"""
# 1. ADD THESE LINES AT THE VERY TOP
import eventlet
eventlet.monkey_patch()

import os
from flask import Flask, send_from_directory, send_file
from flask_cors import CORS
from flask_socketio import SocketIO
from dotenv import load_dotenv
from models import init_db
from routes.user_routes import user_bp
from routes.camera_routes import camera_bp
from routes.monitoring_routes import monitoring_bp
from ai_processor.video_streamer import VideoStreamer

# Load environment variables
load_dotenv()

# Get paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
FRONTEND_BUILD_DIR = os.path.join(PROJECT_ROOT, 'frontend', 'dist')
FRONTEND_INDEX = os.path.join(FRONTEND_BUILD_DIR, 'index.html')

app = Flask(__name__, static_folder=None)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
app.config['MONGODB_URI'] = os.getenv('MONGODB_URI', 'mongodb://127.0.0.1:27017/crowd_density_db')

# Initialize CORS
CORS(app, origins="*", supports_credentials=True)

# Initialize SocketIO for real-time communication
# Using eventlet is recommended for production performance
try:
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
except Exception as e:
    print(f"Warning: Could not use eventlet, falling back to threading mode: {e}")
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Initialize database
init_db(app.config['MONGODB_URI'])

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api/auth')
app.register_blueprint(camera_bp, url_prefix='/api/cameras')
app.register_blueprint(monitoring_bp, url_prefix='/api/monitoring')

# Initialize video streamer (must be after socketio initialization)
video_streamer = VideoStreamer(socketio)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {'status': 'ok', 'message': 'Crowd Density Monitoring API is running'}

# Serve static assets from React build (CSS, JS, images, etc.)
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve static assets from frontend build"""
    if os.path.exists(FRONTEND_BUILD_DIR):
        try:
            return send_from_directory(os.path.join(FRONTEND_BUILD_DIR, 'assets'), filename)
        except:
            return {'error': 'Asset not found'}, 404
    return {'error': 'Assets not found'}, 404

# Catch-all route for frontend (must be LAST - after all API routes)
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve React app for all non-API routes"""
    # Don't serve API routes through this catch-all
    if path.startswith('api'):
        return {'error': 'Not found'}, 404
    # Socket.IO is handled separately, but don't serve it here
    if path.startswith('socket.io'):
        return {'error': 'Socket.IO endpoint'}, 400
    
    # Check if it's a static file (has file extension but not .html)
    if '.' in path and not path.endswith('.html'):
        file_path = os.path.join(FRONTEND_BUILD_DIR, path)
        if os.path.exists(file_path):
            return send_file(file_path)
    
    # For all other routes, serve index.html (React Router handles client-side routing)
    if os.path.exists(FRONTEND_INDEX):
        return send_file(FRONTEND_INDEX)
    return {'error': 'Frontend not built. Run: cd frontend && npm run build'}, 404

@app.route('/')
def root():
    """Root endpoint - serve React app"""
    if os.path.exists(FRONTEND_INDEX):
        return send_file(FRONTEND_INDEX)
    else:
        return {
            'message': 'Crowd Density Monitoring API',
            'status': 'Frontend not built yet',
            'instructions': {
                'option_1': 'Build frontend: cd frontend && npm run build',
                'option_2': 'Run frontend separately: cd frontend && npm run dev (then access http://localhost:3000)'
            },
            'api_endpoints': {
                'health': '/api/health',
                'auth': '/api/auth',
                'cameras': '/api/cameras',
                'monitoring': '/api/monitoring'
            }
        }, 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Check if frontend is built
    frontend_built = os.path.exists(FRONTEND_INDEX)
    
    print("=" * 70)
    print("🚀 Crowd Density Monitoring - Full Stack Application")
    print("=" * 70)
    print(f"✓ Backend API server starting on http://localhost:{port}")
    print(f"✓ API endpoints available at http://localhost:{port}/api/")
    print(f"✓ Health check: http://localhost:{port}/api/health")
    print("-" * 70)
    
    if frontend_built:
        print(f"✓ Frontend build found - serving from {FRONTEND_BUILD_DIR}")
        print(f"✓ Access the FULL application at: http://localhost:{port}")
        print("=" * 70)
    else:
        print("⚠️  Frontend build not found!")
        print("   To build frontend: cd frontend && npm install && npm run build")
        print(f"   Then restart this server to serve both frontend and backend")
        print("-" * 70)
        print("   For now, API is available at http://localhost:{port}/api/")
        print("=" * 70)
    
    print()
    
    # use socketio.run instead of app.run
    socketio.run(app, host='0.0.0.0', port=port, debug=debug, allow_unsafe_werkzeug=True)