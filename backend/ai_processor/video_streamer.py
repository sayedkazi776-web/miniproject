"""
Real-time video streaming with AI processing
"""
import cv2
import base64
import threading
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
                    error_msg = {'message': 'Camera ID required', 'camera_id': None}
                    print(f"✗ {error_msg['message']}")
                    self.socketio.emit('error', error_msg)
                    return
                
                if camera_id in self.active_streams:
                    error_msg = {'message': 'Stream already active', 'camera_id': camera_id}
                    print(f"✗ {error_msg['message']}")
                    self.socketio.emit('error', error_msg)
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
        
        if camera_id in self.active_streams:
            print(f"Stream already active for camera {camera_id}")
            return
        
        # Get camera info
        camera = Camera.find_by_id(camera_id)
        if not camera:
            self.socketio.emit('error', {'message': 'Camera not found'})
            return

        camera_url = camera["url"]
        is_file_source = self._is_video_file_source(camera_url)

        # Create and start stream thread
        stream_thread = threading.Thread(
            target=self._stream_worker,
            args=(camera_id, camera_url, threshold, is_file_source),
            daemon=True,
        )
        stream_thread.start()
        self.active_streams[camera_id] = stream_thread
        
        print(f"Started stream for camera {camera_id}")
    
    def stop_stream(self, camera_id):
        """Stop streaming a camera"""
        if camera_id in self.active_streams:
            # Mark stream as stopped (the worker checks this)
            self.active_streams[camera_id] = None
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
        """
        Resolve a camera URL into an absolute path for a local video file.

        - Absolute paths are used as-is.
        - Relative names/paths are looked up in the project-level "videos" folder.
        """
        url = camera_url.strip()
        # Absolute path (e.g. C:\\videos\\clip.mp4 or /home/user/clip.mp4)
        if os.path.isabs(url):
            return url
        # Otherwise, treat as relative to PROJECT_ROOT/videos
        return os.path.join(VIDEO_DIR, url)

    def _stream_worker(self, camera_id, camera_url, threshold, is_file_source=False):
        """Worker thread for video streaming (camera or video file)"""
        cap = None
        frame_count = 0
        last_log_time = time.time()
        log_interval = 5.0  # Log every 5 seconds
        
        try:
            print(f"Attempting to open video source: {camera_url}")

            # Validate and open video source
            cap = None
            if is_file_source:
                # Treat as local video file
                video_path = self._resolve_video_file_path(camera_url)
                print(f"Opening local video file: {video_path}")
                if not os.path.exists(video_path):
                    error_msg = f'Video file not found: {video_path}'
                    print(f"✗ {error_msg}")
                    try:
                        self.socketio.emit(
                            "error",
                            {
                                "camera_id": camera_id,
                                "message": error_msg,
                            },
                        )
                    except Exception:
                        pass
                    return
                cap = cv2.VideoCapture(video_path)
            elif camera_url and camera_url.strip().isdigit():
                # Webcam index (must be numeric string like "0", "1", "2")
                camera_index = int(camera_url.strip())
                print(f"Opening webcam with index: {camera_index}")
                cap = cv2.VideoCapture(camera_index)
                # Set buffer size to 1 to reduce latency
                if cap.isOpened():
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            elif camera_url and (
                camera_url.startswith("http")
                or camera_url.startswith("rtsp")
                or camera_url.startswith("/")
            ):
                # RTSP URL or file path
                print(f"Opening video source URL: {camera_url}")
                cap = cv2.VideoCapture(camera_url)
                # For RTSP, try to use TCP transport if available (more reliable)
                if camera_url.startswith("rtsp") and cap.isOpened():
                    # Try setting buffer properties for better RTSP performance
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                    # Some RTSP cameras work better with specific backends
                    # FFmpeg backend often handles RTSP better than default
                    # This is a soft setting that won't break if not supported
                    try:
                        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"H264"))
                    except Exception:
                        pass
                elif cap.isOpened():
                    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            else:
                error_msg = (
                    f'Invalid camera URL: "{camera_url}". Use a number (0, 1, 2...) for webcam, '
                    f'RTSP/HTTP URL for IP camera, or a video filename like "demo.mp4" '
                    f'saved in the "videos" folder.'
                )
                print(f"✗ {error_msg}")
                try:
                    self.socketio.emit(
                        "error",
                        {
                            "camera_id": camera_id,
                            "message": error_msg,
                        },
                    )
                except Exception:
                    pass
                return
            
            # Give it a moment to initialize
            time.sleep(0.5)
            
            if not cap or not cap.isOpened():
                if is_file_source:
                    error_msg = f"Could not open video file. Check that it is a valid video: {camera_url}"
                elif camera_url and camera_url.strip().isdigit():
                    error_msg = f'Could not open webcam {camera_url}. Try a different index (0, 1, 2...) or check camera permissions.'
                else:
                    error_msg = f"Could not open video source: {camera_url}. Check if the URL is correct and accessible."
                print(f"✗ {error_msg}")
                try:
                    self.socketio.emit('error', {
                        'camera_id': camera_id,
                        'message': error_msg
                    })
                except:
                    pass
                if cap:
                    cap.release()
                return
            
            print(f"✓ Streaming started for camera {camera_id} from {camera_url}")
            
            consecutive_failures = 0
            max_failures = 10
            
            while camera_id in self.active_streams:
                ret, frame = cap.read()
                if not ret:
                    # For video files, stop cleanly when we reach the end of the file
                    if is_file_source:
                        print(f"✓ Video playback finished for camera {camera_id}")
                        break

                    consecutive_failures += 1
                    if consecutive_failures >= max_failures:
                        print(
                            f"✗ Failed to read {max_failures} consecutive frames from camera {camera_id}"
                        )
                        try:
                            self.socketio.emit(
                                "error",
                                {
                                    "camera_id": camera_id,
                                    "message": "Camera stopped responding. Check if camera is connected and accessible.",
                                },
                            )
                        except Exception:
                            pass
                        break
                    time.sleep(0.1)
                    continue
                
                consecutive_failures = 0  # Reset on successful read
                
                # Process frame with YOLO
                if self.yolo_detector:
                    detections = self.yolo_detector.detect(frame)
                    density_info = self.density_detector.calculate_density(detections, frame.shape)
                    
                    # Draw detections
                    frame = self.yolo_detector.draw_detections(frame, detections)
                    
                    # Draw density overlay
                    frame = self._draw_density_overlay(frame, density_info, threshold)
                    
                    # Check threshold
                    alert_triggered = self.density_detector.check_threshold(
                        density_info['density_value'], 
                        threshold
                    )
                    
                    # Log density data periodically
                    current_time = time.time()
                    if current_time - last_log_time >= log_interval:
                        DensityLog.create(
                            camera_id,
                            density_info['person_count'],
                            density_info['density_value'],
                            alert_triggered
                        )
                        last_log_time = current_time
                    
                    # Encode frame to base64
                    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                    frame_base64 = base64.b64encode(buffer).decode('utf-8')
                    
                    # Emit frame and data
                    try:
                        self.socketio.emit('frame', {
                            'camera_id': camera_id,
                            'frame': frame_base64,
                            'density': density_info,
                            'alert': alert_triggered
                        })
                    except Exception as emit_error:
                        print(f"✗ Error emitting frame: {emit_error}")
                        break
                else:
                    # No YOLO model, send frame without processing
                    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                    frame_base64 = base64.b64encode(buffer).decode('utf-8')
                    
                    try:
                        self.socketio.emit('frame', {
                            'camera_id': camera_id,
                            'frame': frame_base64,
                            'density': {'person_count': 0, 'density_value': 0.0, 'density_per_sqm': 0.0},
                            'alert': False
                        })
                    except Exception as emit_error:
                        print(f"✗ Error emitting frame: {emit_error}")
                        break
                
                frame_count += 1
                # Limit frame rate to ~10 FPS to reduce CPU load
                time.sleep(0.1)
        
        except Exception as e:
            print(f"Error in stream worker for camera {camera_id}: {e}")
            self.socketio.emit('error', {
                'camera_id': camera_id,
                'message': str(e)
            })
        
        finally:
            if cap:
                cap.release()
            if camera_id in self.active_streams:
                del self.active_streams[camera_id]
            print(f"Stream worker stopped for camera {camera_id}")
    
    def _draw_density_overlay(self, frame, density_info, threshold):
        """Draw density information overlay on frame"""
        import cv2
        import numpy as np
        
        # Create overlay
        overlay = frame.copy()
        
        # Background for text
        cv2.rectangle(overlay, (10, 10), (350, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Text color based on alert status
        alert_triggered = density_info['density_value'] >= threshold
        text_color = (0, 0, 255) if alert_triggered else (0, 255, 0)
        
        # Draw text
        cv2.putText(frame, f"People: {density_info['person_count']}", 
                   (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, f"Density: {density_info['density_value']:.2f}", 
                   (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
        cv2.putText(frame, f"Per sqm: {density_info['density_per_sqm']:.2f}", 
                   (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if alert_triggered:
            cv2.putText(frame, "ALERT: OVERCROWDING!", 
                       (20, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        return frame

