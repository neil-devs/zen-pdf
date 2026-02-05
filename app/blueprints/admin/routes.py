from flask import render_template
from flask_login import login_required
from app.blueprints.admin import admin_bp
from app.models.user import User
from app.models.activity_log import ActivityLog
from app.utils.decorators import admin_required

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Fetch stats
    total_users = User.query.count()
    # Fetch last 10 logs, ordered by newest first
    recent_logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                           user_count=total_users, 
                           logs=recent_logs)

@admin_bp.route('/users')
@login_required
@admin_required
def users_list():
    users = User.query.all()
    return render_template('admin/users.html', users=users)