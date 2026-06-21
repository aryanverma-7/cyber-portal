from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from services.password_analyzer import PasswordAnalyzer
import json

bp = Blueprint('password', __name__, url_prefix='/password')

@bp.route('/')
@login_required
def index():
    return render_template('password/index.html')

@bp.route('/check', methods=['POST'])
@login_required
def check_password():
    password = request.json.get('password', '')
    
    analyzer = PasswordAnalyzer()
    result = analyzer.analyze_password(password)
    
    return jsonify(result)

@bp.route('/generator')
@login_required
def generator():
    return render_template('password/generator.html')

@bp.route('/generate-strong', methods=['POST'])
@login_required
def generate_strong_password():
    length = int(request.json.get('length', 16))
    use_upper = request.json.get('use_upper', True)
    use_lower = request.json.get('use_lower', True)
    use_numbers = request.json.get('use_numbers', True)
    use_special = request.json.get('use_special', True)
    
    analyzer = PasswordAnalyzer()
    password = analyzer.generate_password(
        length=length,
        use_upper=use_upper,
        use_lower=use_lower,
        use_numbers=use_numbers,
        use_special=use_special
    )
    
    result = analyzer.analyze_password(password)
    
    return jsonify({
        'password': password,
        'analysis': result
    })