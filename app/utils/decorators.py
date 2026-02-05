from functools import wraps
from flask import abort, session, flash, redirect, url_for
from flask_login import current_user

# --- 1. ADMIN CHECK ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If user is not logged in OR role is not admin, show 403 Forbidden
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# --- 2. GUEST LIMIT CHECK (NEW) ---
def guest_limit_required(f):
    """
    Restricts guest users to 3 tool usages.
    If they are logged in, this check is skipped.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. If user is logged in, Bypass this check (Unlimited Access)
        if current_user.is_authenticated:
            return f(*args, **kwargs)

        # 2. Get current usage count (Default to 0)
        usage_count = session.get('guest_usage_count', 0)

        # 3. If limit reached (3 or more), Block and Redirect
        if usage_count >= 3:
            flash('🔒 Free limit reached (3/3). Create a free account for unlimited access.', 'warning')
            return redirect(url_for('auth.register'))
            
        # 4. If limit is not reached, allow access
        return f(*args, **kwargs)
        
    return decorated_function