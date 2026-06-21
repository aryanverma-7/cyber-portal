from flask import Blueprint, render_template, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from models.report import Report
from models.course import CourseProgress
from models.quiz import QuizScore
from services.report_generator import ReportGenerator
import os

bp = Blueprint('reports', __name__, url_prefix='/reports')

@bp.route('/')
@login_required
def index():
    user_reports = Report.query.filter(
        Report.user_id == current_user.id
    ).order_by(Report.generated_at.desc()).limit(20).all()
    
    return render_template('reports/index.html', reports=user_reports)

@bp.route('/progress')
@login_required
def progress_report():
    return render_template('reports/progress.html')

@bp.route('/generate-progress', methods=['POST'])
@login_required
def generate_progress_report():
    report_type = 'progress'
    title = f'Progress Report - {current_user.get_full_name()}'
    
    generator = ReportGenerator()
    file_path = generator.generate_progress_report(current_user)
    
    report = Report(
        user_id=current_user.id,
        report_type=report_type,
        title=title,
        file_path=file_path
    )
    from models import db
    from config import Config
    db.session.add(report)
    db.session.commit()
    
    flash('Progress report generated successfully', 'success')
    return redirect(url_for('reports.index'))

@bp.route('/quiz')
@login_required
def quiz_report():
    return render_template('reports/quiz.html')

@bp.route('/generate-quiz', methods=['POST'])
@login_required
def generate_quiz_report():
    report_type = 'quiz'
    title = f'Quiz Performance Report - {current_user.get_full_name()}'
    
    generator = ReportGenerator()
    file_path = generator.generate_quiz_report(current_user)
    
    report = Report(
        user_id=current_user.id,
        report_type=report_type,
        title=title,
        file_path=file_path
    )
    
    db.session.add(report)
    db.session.commit()
    
    flash('Quiz report generated successfully', 'success')
    return redirect(url_for('reports.index'))

@bp.route('/download/<int:report_id>')
@login_required
def download_report(report_id):
    report = Report.query.get_or_404(report_id)
    
    if report.user_id != current_user.id and not current_user.is_admin():
        return 'Unauthorized', 403
    
    file_path = os.path.join(Config.REPORTS_DIR, report.file_path)
    
    if not os.path.exists(file_path):
        flash('Report file not found', 'error')
        return redirect(url_for('reports.index'))
    
    return send_file(
        file_path,
        as_download=True,
        download_name=report.title
    )