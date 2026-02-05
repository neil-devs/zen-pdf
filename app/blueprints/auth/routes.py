from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.blueprints.auth import auth_bp
from app.blueprints.auth.forms import RegistrationForm, LoginForm
from app.models.user import User
from app.models.activity_log import ActivityLog

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('core.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create hashed password is handled by the model
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        # Log the activity
        log = ActivityLog(user_id=user.id, action='REGISTER', ip_address=request.remote_addr)
        db.session.add(log)
        db.session.commit()

        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('core.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            
            # Log the success
            log = ActivityLog(user_id=user.id, action='LOGIN', ip_address=request.remote_addr)
            db.session.add(log)
            db.session.commit()
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('core.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('auth/login.html', title='Login', form=form)

@auth_bp.route('/logout')
def logout():
    if current_user.is_authenticated:
        # Log the logout before destroying session
        log = ActivityLog(user_id=current_user.id, action='LOGOUT', ip_address=request.remote_addr)
        db.session.add(log)
        db.session.commit()
        
    logout_user()
    return redirect(url_for('core.landing'))