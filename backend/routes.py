from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

# Change 1: Use absolute imports
from models import db, User, TeacherProfile, Student, Class, Attendance, Holiday
from auth import check_credentials

bp = Blueprint('api', __name__)


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = check_credentials(username, password)
    if user:
        # In a real app, you would return a JWT token here
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'role': user.role
            }
        }), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


@bp.route('/teacher/signup', methods=['POST'])
def teacher_signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    full_name = data.get('full_name')

    if not all([username, password, full_name]):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409

    # Create user entry
    new_user = User(username=username, role='teacher')
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()  # Commit to get the user ID

    # Create teacher profile entry
    new_teacher_profile = TeacherProfile(
        user_id=new_user.id,
        full_name=full_name,
        is_approved=False
    )
    db.session.add(new_teacher_profile)
    db.session.commit()

    return jsonify({'message': 'Registration request sent. Waiting for admin approval.'}), 201


# --- Admin Routes ---
@bp.route('/admin/pending-teachers', methods=['GET'])
def get_pending_teachers():
    # This is a simplified query. A real app would use joins.
    pending_teachers = TeacherProfile.query.filter_by(is_approved=False).all()
    teachers_list = [{
        'id': teacher.user_id,
        'full_name': teacher.full_name
    } for teacher in pending_teachers]
    return jsonify(teachers_list)

# --- NEW ROUTE ADDED HERE ---
@bp.route('/admin/approve-teacher/<int:teacher_id>', methods=['POST'])
def approve_teacher(teacher_id):
    teacher_profile = TeacherProfile.query.filter_by(user_id=teacher_id).first()
    if not teacher_profile:
        return jsonify({'error': 'Teacher not found'}), 404
    
    teacher_profile.is_approved = True
    db.session.commit()
    
    return jsonify({'message': f'Teacher {teacher_profile.full_name} approved successfully.'}), 200


# --- Teacher Routes ---
@bp.route('/teacher/students', methods=['GET'])
def get_students():
    # For now, mocking data. Later, this will fetch from the database.
    # class_id = request.args.get('class_id')
    mock_students = [
        {"id": 1, "full_name": "Alice Johnson", "roll_number": 101},
        {"id": 2, "full_name": "Bob Williams", "roll_number": 102},
        {"id": 3, "full_name": "Charlie Brown", "roll_number": 103},
    ]
    return jsonify(mock_students)


@bp.route('/teacher/attendance', methods=['POST'])
def save_attendance():
    data = request.get_json()
    # In a real app, you would save data['date'] and data['attendance'] to the DB
    print("Received attendance data:", data)
    return jsonify({'message': 'Attendance saved successfully!'}), 200


# --- Student Routes ---
@bp.route('/student/dashboard', methods=['GET'])
def get_student_dashboard():
    # student_id = request.args.get('student_id')
    # Mock data for the student dashboard
    mock_data = {
        "total_present": 85,
        "total_absent": 10,
        "total_half_day": 5,
        "total_working_days": 100
    }
    return jsonify(mock_data)
