"""
YOLOv8 Model wrapper for person detection
"""
from ultralytics import YOLO
import os

class YOLOPersonDetector:
    """YOLOv8-based person detector"""
    
    def __init__(self, model_path=None):
        """
        Initialize YOLO model for person detection
        
        Args:
            model_path: Path to YOLOv8 model weights. If None, uses default 'yolov8n.pt'
        """
        if model_path is None:
            # Use nano model for faster inference
            model_path = 'yolov8n.pt'
        
        self.model = YOLO(model_path)
        self.person_class_id = 0  # COCO dataset class 0 is 'person'
    
    def detect(self, frame, conf_threshold=0.25):
        """
        Detect people in a frame
        
        Args:
            frame: OpenCV frame (numpy array)
            conf_threshold: Confidence threshold for detections
        
        Returns:
            List of detections: [{'bbox': [x1, y1, x2, y2], 'confidence': float}, ...]
        """
        results = self.model(frame, conf=conf_threshold, classes=[self.person_class_id], verbose=False)
        
        detections = []
        if len(results) > 0 and results[0].boxes is not None:
            boxes = results[0].boxes
            for i in range(len(boxes)):
                box = boxes[i]
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = float(box.conf[0].cpu().numpy())
                
                detections.append({
                    'bbox': [int(x1), int(y1), int(x2), int(y2)],
                    'confidence': confidence
                })
        
        return detections
    
    def draw_detections(self, frame, detections):
        """
        Draw bounding boxes on frame
        
        Args:
            frame: OpenCV frame
            detections: List of detections from detect() method
        
        Returns:
            Frame with drawn bounding boxes
        """
        import cv2
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            confidence = det['confidence']
            
            # Draw bounding box (blue color)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 100, 0), 2)
            
            # Draw confidence label
            label = f'Person {confidence:.2f}'
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(frame, (x1, y1 - label_size[1] - 10), 
                         (x1 + label_size[0], y1), (255, 100, 0), -1)
            cv2.putText(frame, label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame

