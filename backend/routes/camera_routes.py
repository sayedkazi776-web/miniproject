"""
Camera management routes
"""
from flask import Blueprint, request, jsonify
from models import Camera
from auth import auth_required
from bson import ObjectId

camera_bp = Blueprint('camera', __name__)

@camera_bp.route('', methods=['GET'])
@auth_required
def get_cameras():
    """Get all cameras"""
    try:
        cameras = Camera.find_all()
        return jsonify({
            'cameras': [{
                'id': str(cam['_id']),
                'name': cam['name'],
                'url': cam['url'],
                'location': cam.get('location', ''),
                'owner_id': str(cam.get('owner_id', ''))
            } for cam in cameras]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@camera_bp.route('', methods=['POST'])
@auth_required
def create_camera():
    """Create a new camera"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        url = data.get('url', '').strip()
        location = data.get('location', '').strip()
        
        if not name or not url:
            return jsonify({'error': 'Name and URL are required'}), 400
        
        # Validate camera URL format
        url_lower = url.lower().strip()
        video_exts = ('.mp4', '.avi', '.mov', '.mkv', '.flv')
        is_video_file = url_lower.endswith(video_exts)

        if not (
            url.isdigit()
            or url_lower.startswith('http://')
            or url_lower.startswith('https://')
            or url_lower.startswith('rtsp://')
            or url.startswith('/')
            or url.startswith('\\')
            or is_video_file
        ):
            return jsonify({
                'error': (
                    f'Invalid camera URL: "{url}". '
                    f'Use a number (0, 1, 2...) for webcam, RTSP/HTTP URL for IP camera, '
                    f'or a video filename like "demo.mp4" placed in the project "videos" folder.'
                )
            }), 400
        
        user_id = request.user['user_id']
        camera_id = Camera.create(name, url, location, user_id)
        
        if not camera_id:
            return jsonify({'error': 'Failed to create camera. Name might already exist.'}), 400
        
        return jsonify({
            'message': 'Camera created successfully',
            'camera': {
                'id': camera_id,
                'name': name,
                'url': url,
                'location': location
            }
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@camera_bp.route('/<camera_id>', methods=['GET'])
@auth_required
def get_camera(camera_id):
    """Get a specific camera"""
    try:
        camera = Camera.find_by_id(camera_id)
        if not camera:
            return jsonify({'error': 'Camera not found'}), 404
        
        return jsonify({
            'camera': {
                'id': str(camera['_id']),
                'name': camera['name'],
                'url': camera['url'],
                'location': camera.get('location', ''),
                'owner_id': str(camera.get('owner_id', ''))
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@camera_bp.route('/<camera_id>', methods=['PUT'])
@auth_required
def update_camera(camera_id):
    """Update a camera"""
    try:
        data = request.get_json()
        updates = {}
        
        if 'name' in data:
            updates['name'] = data['name'].strip()
        if 'url' in data:
            url = data['url'].strip()
            # Validate camera URL format
            url_lower = url.lower()
            video_exts = ('.mp4', '.avi', '.mov', '.mkv', '.flv')
            is_video_file = url_lower.endswith(video_exts)

            if not (
                url.isdigit()
                or url_lower.startswith('http://')
                or url_lower.startswith('https://')
                or url_lower.startswith('rtsp://')
                or url.startswith('/')
                or url.startswith('\\')
                or is_video_file
            ):
                return jsonify({
                    'error': (
                        f'Invalid camera URL: "{url}". '
                        f'Use a number (0, 1, 2...) for webcam, RTSP/HTTP URL for IP camera, '
                        f'or a video filename like "demo.mp4" placed in the project "videos" folder.'
                    )
                }), 400
            updates['url'] = url
        if 'location' in data:
            updates['location'] = data['location'].strip()
        
        if not updates:
            return jsonify({'error': 'No valid fields to update'}), 400
        
        success = Camera.update(camera_id, updates)
        if not success:
            return jsonify({'error': 'Camera not found or update failed'}), 404
        
        camera = Camera.find_by_id(camera_id)
        return jsonify({
            'message': 'Camera updated successfully',
            'camera': {
                'id': str(camera['_id']),
                'name': camera['name'],
                'url': camera['url'],
                'location': camera.get('location', '')
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@camera_bp.route('/<camera_id>', methods=['DELETE'])
@auth_required
def delete_camera(camera_id):
    """Delete a camera"""
    try:
        success = Camera.delete(camera_id)
        if not success:
            return jsonify({'error': 'Camera not found'}), 404
        
        return jsonify({'message': 'Camera deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

