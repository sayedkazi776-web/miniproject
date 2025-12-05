"""
Crowd density calculation and analysis
"""
import cv2
import numpy as np

class DensityDetector:
    """Calculate crowd density from person detections"""
    
    def __init__(self, reference_area_sqm=100.0):
        """
        Initialize density detector
        
        Args:
            reference_area_sqm: Reference area in square meters for density calculation
                                This is an approximation - adjust based on camera calibration
        """
        self.reference_area_sqm = reference_area_sqm
    
    def calculate_density(self, detections, frame_shape):
        """
        Calculate crowd density from detections
        
        Args:
            detections: List of person detections
            frame_shape: Shape of the frame (height, width)
        
        Returns:
            dict with 'person_count', 'density_value', 'density_per_sqm'
        """
        person_count = len(detections)
        
        # Calculate approximate area covered by detections
        # This is a simplified approach - for production, use camera calibration
        if person_count == 0:
            return {
                'person_count': 0,
                'density_value': 0.0,
                'density_per_sqm': 0.0
            }
        
        # Estimate frame area in "person units" based on average detection size
        frame_height, frame_width = frame_shape[:2]
        frame_area_pixels = frame_height * frame_width
        
        # Average detection area (approximation)
        total_detection_area = 0
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            area = (x2 - x1) * (y2 - y1)
            total_detection_area += area
        
        avg_detection_area = total_detection_area / person_count if person_count > 0 else 0
        
        # Estimate ground area (simplified - assumes detections represent ~1-2 sqm per person)
        # This is a heuristic and should be calibrated for real-world use
        estimated_ground_area = (frame_area_pixels / avg_detection_area) * 1.5 if avg_detection_area > 0 else self.reference_area_sqm
        
        # Convert to square meters (rough approximation)
        # For production, implement proper camera calibration
        area_sqm = (estimated_ground_area / 100.0) * self.reference_area_sqm
        
        # Calculate density (people per square meter)
        density_per_sqm = person_count / area_sqm if area_sqm > 0 else 0
        
        # Normalized density value (0-1 scale, where 1 = very dense)
        # Assuming >2 people/sq m is very dense
        density_value = min(density_per_sqm / 2.0, 1.0)
        
        return {
            'person_count': person_count,
            'density_value': round(density_value, 3),
            'density_per_sqm': round(density_per_sqm, 2)
        }
    
    def check_threshold(self, density_value, threshold=0.65):
        """
        Check if density exceeds threshold
        
        Args:
            density_value: Normalized density value (0-1)
            threshold: Alert threshold (0-1)
        
        Returns:
            Boolean indicating if threshold is exceeded
        """
        return density_value >= threshold

