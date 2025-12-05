"""
Real-time video streaming with AI processing
"""
import cv2
import base64
import time
import sys
import os
# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Camera, DensityLog
from ai_processor.yolo_model import YOLOPersonDetector
from ai_processor.density_detector import DensityDetector

# Paths for resolving local video files
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
VIDEO_DIR = os.path.join(PROJECT_ROOT, "videos")

class VideoStreamer:
    """Handle real-time video streaming and processing"""
    
    def __init__(self, socketio, density_threshold=0.65):
        """
        Initialize video streamer
        
        Args:
            socketio: Flask-SocketIO instance
            density_threshold: Default density threshold for alerts
        """
        self.socketio = socketio
        self.density_threshold = density_threshold
        self.active_streams = {}  # {camera_id: stream_thread}
        self.stream_signals = {}  # {camera_id: boolean} - True to keep running
        self.yolo_detector = None
        self.density_detector = DensityDetector()
        
        # Initialize YOLO model (lazy loading)
        self._init_yolo()
        
        # Register SocketIO events
        self._register_events()
    
    def _init_yolo(self):
        """Initialize YOLO model"""
        try:
            self.yolo_detector = YOLOPersonDetector()
            print("YOLOv8 model loaded successfully")
        except Exception as e:
            print(f"Warning: Could not load YOLO model: {e}")
            print("Please ensure ultralytics is installed and yolov8n.pt is available")
    
    def _register_events(self):
        """Register SocketIO event handlers"""
        
        @self.socketio.on('connect')
        def handle_connect():
            print(f"✓ Client connected to video streamer")
            self.socketio.emit('connected', {'message': 'Connected to video streamer'})
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            print("Client disconnected")
        
        @self.socketio.on('start_stream')
        def handle_start_stream(data):
            """Start streaming a camera"""
            try:
                camera_id = data.get('camera_id')
                threshold = data.get('threshold', self.density_threshold)
                
                print(f"Received start_stream request for camera: {camera_id}")
                
                if not camera_id:
                    self.socketio.emit('error', {'message': 'Camera ID required'})
                    return
                
                if camera_id in self.active_streams:
                    # Stream already running, just update threshold? 
                    # For now we can ignore or restart. Let's restart logic safely.
                    print(f"Stream already active for camera {camera_id}")
                    return
                
                print(f"✓ Starting stream for camera: {camera_id}")
                self.start_stream(camera_id, threshold)
            except Exception as e:
                print(f"✗ Error in start_stream handler: {e}")
                self.socketio.emit('error', {'message': f'Error starting stream: {str(e)}'})
        
        @self.socketio.on('stop_stream')
        def handle_stop_stream(data):
            """Stop streaming a camera"""
            camera_id = data.get('camera_id')
            if camera_id:
                self.stop_stream(camera_id)
    
    def start_stream(self, camera_id, threshold=None):
        """Start streaming a camera or video file"""
        if threshold is None:
            threshold = self.density_threshold
        
        # Set running signal
        self.stream_signals[camera_id] = True
        
        # Get camera info
        camera = Camera.find_by_id(camera_id)
        if not camera:
            self.socketio.emit('error', {'message': 'Camera not found'})
            return

        camera_url = camera["url"]
        is_file_source = self._is_video_file_source(camera_url)

        # Use socketio.start_background_task instead of threading.Thread
        # This is CRITICAL for working with eventlet/gevent
        stream_task = self.socketio.start_background_task(
            target=self._stream_worker,
            camera_id=camera_id,
            camera_url=camera_url,
            threshold=threshold,
            is_file_source=is_file_source
        )
        
        self.active_streams[camera_id] = stream_task
        print(f"Started stream task for camera {camera_id}")
    
    def stop_stream(self, camera_id):
        """Stop streaming a camera"""
        if camera_id in self.stream_signals:
            # Signal the worker loop to stop
            self.stream_signals[camera_id] = False
            
            # Clean up references
            if camera_id in self.active_streams:
                del self.active_streams[camera_id]
            
            print(f"Stopped stream for camera {camera_id}")
    
    def _is_video_file_source(self, camera_url: str) -> bool:
        """Return True if the URL should be treated as a local video file path."""
        if not camera_url:
            return False
        url = camera_url.strip()
        # If it looks like a webcam index or network URL, it's not a file
        if url.isdigit():
            return False
        if url.startswith("http://") or url.startswith("https://") or url.startswith("rtsp://"):
            return False
        # Common video file extensions
        video_exts = (".mp4", ".avi", ".mov", ".mkv", ".flv")
        return url.lower().endswith(video_exts)

    def _resolve_video_file_path(self, camera_url: str) -> str:
        """Resolve a camera URL into an absolute path for a local video file."""
        url = camera_url.strip()
        if os.path.isabs(url):
            return url
        return os.path.join(VIDEO_DIR, url)

    def _stream_worker(self, camera_id, camera_url, threshold, is_file_source=False):
        """Worker thread for video streaming (camera or video file)"""
        cap = None
        last_log_time = time.time()
        log_interval = 5.0  # Log every 5 seconds
        
        try:
            print(f"Attempting to open video source: {camera_url}")

            # Validate and open video source
            if is_file_source:
                video_path = self._resolve_video_file_path(camera_url)
                if not os.path.exists(video_path):
                    self.socketio.emit("error", {"camera_id": camera_id, "message": f"File not found: {video_path}"})
                    return
                cap = cv2.VideoCapture(video_path)
            elif camera_url and camera_url.strip().isdigit():
                # Webcam
                camera_index = int(camera_url.strip())
                cap = cv2.VideoCapture(camera_index)
                if cap.isOpened():
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            else:
                # RTSP/HTTP
                cap = cv2.VideoCapture(camera_url)
                if cap.isOpened():
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            # Give it a moment to initialize - Use socketio.sleep for async compatibility
            self.socketio.sleep(0.5)
            
            if not cap or not cap.isOpened():
                error_msg = f"Could not open video source: {camera_url}"
                print(f"✗ {error_msg}")
                self.socketio.emit('error', {'camera_id': camera_id, 'message': error_msg})
                return
            
            print(f"✓ Streaming started for camera {camera_id}")
            
            consecutive_failures = 0
            
            # Use the signal flag to control the loop
            while self.stream_signals.get(camera_id, False):
                ret, frame = cap.read()
                
                if not ret:
                    if is_file_source:
                        # Restart video file loop
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue
                    
                    consecutive_failures += 1
                    if consecutive_failures >= 10:
                        print(f"✗ Connection lost to camera {camera_id}")
                        self.socketio.emit("error", {"camera_id": camera_id, "message": "Connection lost"})
                        break
                    self.socketio.sleep(0.1)
                    continue
                
                consecutive_failures = 0
                
                # Resize large frames to improve performance
                if frame.shape[1] > 800:
                    scale = 800 / frame.shape[1]
                    frame = cv2.resize(frame, None, fx=scale, fy=scale)

                # Process frame with YOLO
                if self.yolo_detector:
                    detections = self.yolo_detector.detect(frame)
                    density_info = self.density_detector.calculate_density(detections, frame.shape)
                    
                    # Draw
                    frame = self.yolo_detector.draw_detections(frame, detections)
                    frame = self._draw_density_overlay(frame, density_info, threshold)
                    
                    # Alert check
                    alert_triggered = self.density_detector.check_threshold(density_info['density_value'], threshold)
                    
                    # Log to DB
                    current_time = time.time()
                    if current_time - last_log_time >= log_interval:
                        DensityLog.create(camera_id, density_info['person_count'], density_info['density_value'], alert_triggered)
                        last_log_time = current_time
                    
                    # Encode
                    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 70])
                    frame_base64 = base64.b64encode(buffer).decode('utf-8')
                    
                    # Emit
                    self.socketio.emit('frame', {
                        'camera_id': camera_id,
                        'frame': frame_base64,
                        'density': density_info,
                        'alert': alert_triggered
                    })
                
                # Limit FPS to ~10-15 to save CPU and Network
                # Use socketio.sleep instead of time.sleep
                self.socketio.sleep(0.08)
        
        except Exception as e:
            print(f"Error in stream worker: {e}")
            self.socketio.emit('error', {'camera_id': camera_id, 'message': str(e)})
        
        finally:
            if cap:
                cap.release()
            # Clean up signal if it exists
            if camera_id in self.stream_signals:
                del self.stream_signals[camera_id]
            print(f"Stream worker stopped for camera {camera_id}")
    
    def _draw_density_overlay(self, frame, density_info, threshold):
        """Draw density information overlay on frame"""
        # Create overlay
        overlay = frame.copy()
        
        # Background for text
        cv2.rectangle(overlay, (10, 10), (300, 100), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Text color based on alert status
        alert_triggered = density_info['density_value'] >= threshold
        text_color = (0, 0, 255) if alert_triggered else (0, 255, 0)
        
        cv2.putText(frame, f"People: {density_info['person_count']}", 
                   (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, f"Density: {density_info['density_value']:.2f}", 
                   (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
        
        if alert_triggered:
            cv2.putText(frame, "ALERT: OVERCROWDING!", 
                       (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        return frame