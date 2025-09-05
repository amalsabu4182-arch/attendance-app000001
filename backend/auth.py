# Change 1: Use absolute import
from models import User

def check_credentials(username, password):
    """
    Checks if a username and password are valid.
    Returns the User object if valid, None otherwise.
    """
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Additional check for teachers to see if they are approved
        if user.role == 'teacher':
            if hasattr(user, 'teacher_profile') and user.teacher_profile.is_approved:
                return user
            else:
                return None # Teacher exists but is not approved
        return user # Admin or student
    return None

