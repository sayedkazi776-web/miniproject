"""
User authentication routes
"""
from flask import Blueprint, request, jsonify
from models import User
from auth import hash_password, verify_password, create_token, auth_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        name = data.get('name', '').strip()
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Check if user already exists
        existing_user = User.find_by_email(email)
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 400
        
        # Create new user
        password_hash = hash_password(password)
        user_id = User.create(email, password_hash, name)
        
        if not user_id:
            return jsonify({'error': 'Failed to create user. Please check database connection.'}), 500
        
        # Generate token
        token = create_token(user_id, email)
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': {
                'id': user_id,
                'email': email,
                'name': name
            }
        }), 201
    
    except Exception as e:
        error_msg = str(e)
        print(f"Registration error: {error_msg}")  # Log for debugging
        return jsonify({'error': f'Registration failed: {error_msg}'}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find user
        user = User.find_by_email(email)
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate token
        token = create_token(str(user['_id']), user['email'])
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': str(user['_id']),
                'email': user['email'],
                'name': user.get('name', '')
            }
        }), 200
    
    except Exception as e:
        error_msg = str(e)
        print(f"Login error: {error_msg}")  # Log for debugging
        return jsonify({'error': f'Login failed: {error_msg}'}), 500

@user_bp.route('/me', methods=['GET'])
@auth_required
def get_current_user():
    """Get current user info"""
    try:
        user = User.find_by_id(request.user['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': str(user['_id']),
                'email': user['email'],
                'name': user.get('name', '')
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

