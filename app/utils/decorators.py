from functools import wraps
from flask_login import current_user
from flask import abort

def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "staff":
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function