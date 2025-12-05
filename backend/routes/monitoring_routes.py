"""
Monitoring and density logging routes
"""
from flask import Blueprint, request, jsonify
from models import Camera, DensityLog
from auth import auth_required

monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/density/<camera_id>', methods=['GET'])
@auth_required
def get_density_history(camera_id):
    """Get density history for a camera"""
    try:
        # Verify camera exists
        camera = Camera.find_by_id(camera_id)
        if not camera:
            return jsonify({'error': 'Camera not found'}), 404
        
        # Get query parameters
        limit = request.args.get('limit', 100, type=int)
        minutes = request.args.get('minutes', 60, type=int)
        
        if minutes > 0:
            logs = DensityLog.find_recent_by_camera(camera_id, minutes)
        else:
            logs = DensityLog.find_by_camera(camera_id, limit)
        
        return jsonify({
            'camera_id': camera_id,
            'logs': [{
                'id': str(log['_id']),
                'timestamp': log['timestamp'].isoformat(),
                'person_count': log['person_count'],
                'density_value': log['density_value'],
                'alert_triggered': log.get('alert_triggered', False)
            } for log in logs]
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@monitoring_bp.route('/start/<camera_id>', methods=['POST'])
@auth_required
def start_monitoring(camera_id):
    """Start monitoring a camera"""
    try:
        camera = Camera.find_by_id(camera_id)
        if not camera:
            return jsonify({'error': 'Camera not found'}), 404
        
        # The actual streaming is handled by WebSocket
        return jsonify({
            'message': 'Monitoring started',
            'camera_id': camera_id
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@monitoring_bp.route('/stop/<camera_id>', methods=['POST'])
@auth_required
def stop_monitoring(camera_id):
    """Stop monitoring a camera"""
    try:
        # The actual streaming stop is handled by WebSocket
        return jsonify({
            'message': 'Monitoring stopped',
            'camera_id': camera_id
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

