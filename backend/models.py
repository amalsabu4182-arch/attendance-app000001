from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the database instance
db = SQLAlchemy()


# Define the User model for all roles
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    # Roles: 'admin', 'teacher', 'student'
    role = db.Column(db.String(20), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Define the Class model
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    teacher = db.relationship('User', backref=db.backref('assigned_class', uselist=False))
    students = db.relationship('Student', backref='class_ref', lazy=True)


# Define the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # The user_id links to the student's own login credentials in the User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    full_name = db.Column(db.String(120), nullable=False)
    roll_number = db.Column(db.Integer, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('student_profile', uselist=False))


# Define the TeacherProfile model for teacher-specific data
class TeacherProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    is_approved = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship('User', backref=db.backref('teacher_profile', uselist=False))


# Define the Attendance model
class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    # Status can be 'present', 'half-day', 'absent'
    status = db.Column(db.String(20), nullable=False)

    student = db.relationship('Student', backref='attendances')


# Define the Holiday model
class Holiday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    description = db.Column(db.String(200), nullable=False)

