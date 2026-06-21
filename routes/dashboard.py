from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models.user import User
from models.course import Course, CourseProgress
from models.quiz import QuizScore, QuizQuestion
from models.phishing import PhishingCase
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from models.ai_cache import AICache

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def index():
    # User statistics
    total_courses = Course.query.filter(Course.is_published == True).count()
    total_questions = QuizQuestion.query.filter(QuizQuestion.is_active == True).count()
    total_users = User.query.filter(User.is_active == True).count()
    
    # User's progress
    user_courses = CourseProgress.query.filter(
        CourseProgress.user_id == current_user.id
    ).all()
    
    completed_courses = sum(1 for c in user_courses if c.is_completed)
    in_progress_courses = len(user_courses) - completed_courses
    
    # Recent quiz scores
    recent_scores = QuizScore.query.filter(
        QuizScore.user_id == current_user.id
    ).order_by(QuizScore.submitted_at.desc()).limit(5).all()
    
    # Recent phishing checks
    recent_phishing = PhishingCase.query.filter(
        PhishingCase.user_id == current_user.id
    ).order_by(PhishingCase.created_at.desc()).limit(5).all()
    
    # Total points
    total_points = current_user.get_total_points()
    
    return render_template('dashboard/index.html',
                         total_courses=total_courses,
                         total_questions=total_questions,
                         total_users=total_users,
                         completed_courses=completed_courses,
                         in_progress_courses=in_progress_courses,
                         recent_scores=recent_scores,
                         recent_phishing=recent_phishing,
                         total_points=total_points)

@bp.route('/admin')
@login_required
def admin():
    if not current_user.is_admin():
        return render_template('errors/403.html'), 403
    
    # Admin statistics
    total_users = User.query.count()
    active_users = User.query.filter(User.is_active == True).count()
    total_courses = Course.query.count()
    published_courses = Course.query.filter(Course.is_published == True).count()
    total_questions = QuizQuestion.query.count()
    active_questions = QuizQuestion.query.filter(QuizQuestion.is_active == True).count()
    total_phishing_checks = PhishingCase.query.count()
    
    # Recent registrations
    recent_registrations = User.query.order_by(
        User.created_at.desc()
    ).limit(10).all()
    
    # Top users by points
    top_users = User.query.limit(10).all()
    
    return render_template('dashboard/admin.html',
                         total_users=total_users,
                         active_users=active_users,
                         total_courses=total_courses,
                         published_courses=published_courses,
                         total_questions=total_questions,
                         active_questions=active_questions,
                         total_phishing_checks=total_phishing_checks,
                         recent_registrations=recent_registrations,
                         top_users=top_users)

@bp.route('/learning-path')
@login_required
def learning_path():
    # Get user's learning path based on progress
    user_courses = CourseProgress.query.filter(
        CourseProgress.user_id == current_user.id
    ).all()
    
    course_ids = [c.course_id for c in user_courses]
    
    # Available courses
    available_courses = Course.query.filter(
        Course.is_published == True,
        Course.id.notin_(course_ids)
    ).order_by(Course.level, Course.category).all()
    
    # Group by level
    beginner_courses = [c for c in available_courses if c.level == 'beginner']
    intermediate_courses = [c for c in available_courses if c.level == 'intermediate']
    advanced_courses = [c for c in available_courses if c.level == 'advanced']
    
    return render_template('dashboard/learning_path.html',
                         beginner_courses=beginner_courses,
                         intermediate_courses=intermediate_courses,
                         advanced_courses=advanced_courses,
                         user_courses=user_courses)