from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from models import db
from models.user import User
from datetime import datetime, timedelta
import uuid

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        
        # Validation
        if not all([username, email, password, first_name, last_name]):
            flash('Please fill in all fields', 'error')
            return render_template('auth/register.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters', 'error')
            return render_template('auth/register.html')
        
        # Check if user exists
        existing_user = User.query.filter(
            or_(User.username == username, User.email == email)
        ).first()
        
        if existing_user:
            flash('Username or email already exists', 'error')
            return render_template('auth/register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role='student'
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'error')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not all([username, password]):
            flash('Please fill in all fields', 'error')
            return render_template('auth/login.html')
        
        # Find user by username or email
        user = User.query.filter(
            or_(User.username == username, User.email == username)
        ).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated', 'error')
                return render_template('auth/login.html')
            
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(url_for('dashboard.index'))
        
        flash('Invalid username or password', 'error')
        return render_template('auth/login.html')
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('auth.login'))

@bp.route('/reset-password/request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        
        user = User.query.filter(User.email == email).first()
        
        if not user:
            flash('Email not found', 'error')
            return render_template('auth/reset_password_request.html')
        
        # Generate reset token
        token = uuid.uuid4().hex
        user.password_reset_token = token
        user.password_reset_expires = datetime.utcnow() + timedelta(hours=2)
        db.session.commit()
        
        # TODO: Send email with reset link
        reset_link = url_for('auth.reset_password', token=token, _external=True)
        flash(f'Password reset link created: {reset_link}', 'success')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password_request.html')

@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter(User.password_reset_token == token).first()
    
    if not user:
        flash('Invalid reset token', 'error')
        return redirect(url_for('auth.reset_password_request'))
    
    if user.password_reset_expires < datetime.utcnow():
        flash('Reset token has expired', 'error')
        return redirect(url_for('auth.reset_password_request'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        if len(password) < 8:
            flash('Password must be at least 8 characters', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        user.set_password(password)
        user.password_reset_token = None
        user.password_reset_expires = None
        db.session.commit()
        
        flash('Password reset successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', token=token)

@bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')

@bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    bio = request.form.get('bio', '').strip()
    organization = request.form.get('organization', '').strip()
    
    current_user.first_name = first_name
    current_user.last_name = last_name
    current_user.bio = bio
    current_user.organization = organization
    
    db.session.commit()
    flash('Profile updated successfully', 'success')
    return redirect(url_for('auth.profile'))