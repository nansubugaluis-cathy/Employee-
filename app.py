from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee_training.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ==================== DATABASE MODELS ====================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    is_admin = db.Column(db.Boolean, default=False)
    department = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    enrollments = db.relationship('Enrollment', backref='user', lazy=True)
    quiz_attempts = db.relationship('QuizAttempt', backref='user', lazy=True)
    certificates = db.relationship('Certificate', backref='user', lazy=True)

class TrainingModule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    duration_minutes = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    enrollments = db.relationship('Enrollment', backref='module', lazy=True)
    quiz = db.relationship('Quiz', backref='module', uselist=False)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('training_module.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    is_completed = db.Column(db.Boolean, default=False)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'module_id', name='unique_enrollment'),)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('training_module.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    passing_score = db.Column(db.Integer, default=70)  # percentage
    
    questions = db.relationship('QuizQuestion', backref='quiz', lazy=True, cascade='all, delete-orphan')
    attempts = db.relationship('QuizAttempt', backref='quiz', lazy=True)

class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20))  # multiple_choice, true_false
    options = db.Column(db.Text)  # JSON format
    correct_answer = db.Column(db.String(500), nullable=False)

class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Float)  # percentage
    passed = db.Column(db.Boolean, default=False)
    answers = db.Column(db.Text)  # JSON format of user answers

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('training_module.id'), nullable=False)
    issued_at = db.Column(db.DateTime, default=datetime.utcnow)
    certificate_number = db.Column(db.String(100), unique=True)
    
    module = db.relationship('TrainingModule')

# ==================== LOGIN MANAGER ====================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== ROUTES - AUTH ====================

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('employee_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.is_admin:
                return jsonify({'redirect': url_for('admin_dashboard')})
            else:
                return jsonify({'redirect': url_for('employee_dashboard')})
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ==================== ROUTES - EMPLOYEE ====================

@app.route('/employee/dashboard')
@login_required
def employee_dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    certificates = Certificate.query.filter_by(user_id=current_user.id).all()
    
    return render_template('employee_dashboard.html', 
                         enrollments=enrollments,
                         certificates=certificates)

@app.route('/employee/module/<int:module_id>')
@login_required
def view_module(module_id):
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    module = TrainingModule.query.get(module_id)
    if not module:
        return "Module not found", 404
    
    enrollment = Enrollment.query.filter_by(
        user_id=current_user.id,
        module_id=module_id
    ).first()
    
    if not enrollment:
        enrollment = Enrollment(user_id=current_user.id, module_id=module_id)
        db.session.add(enrollment)
        db.session.commit()
    
    return render_template('view_module.html', module=module, enrollment=enrollment)

@app.route('/employee/quiz/<int:quiz_id>')
@login_required
def take_quiz(quiz_id):
    if current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return "Quiz not found", 404
    
    return render_template('take_quiz.html', quiz=quiz)

@app.route('/api/quiz/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    data = request.json
    answers = data.get('answers', {})
    
    # Calculate score
    questions = QuizQuestion.query.filter_by(quiz_id=quiz_id).all()
    correct_count = 0
    
    for question in questions:
        user_answer = answers.get(str(question.id), '')
        if str(user_answer).strip() == str(question.correct_answer).strip():
            correct_count += 1
    
    score = (correct_count / len(questions) * 100) if questions else 0
    passed = score >= quiz.passing_score
    
    # Create quiz attempt record
    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz_id,
        score=score,
        passed=passed,
        answers=json.dumps(answers)
    )
    db.session.add(attempt)
    
    # If passed, mark module as completed and create certificate
    if passed:
        enrollment = Enrollment.query.filter_by(
            user_id=current_user.id,
            module_id=quiz.module_id
        ).first()
        
        if enrollment:
            enrollment.is_completed = True
            enrollment.completed_at = datetime.utcnow()
        
        # Generate certificate
        cert_number = f"CERT-{quiz.module_id}-{current_user.id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        certificate = Certificate(
            user_id=current_user.id,
            module_id=quiz.module_id,
            certificate_number=cert_number
        )
        db.session.add(certificate)
    
    db.session.commit()
    
    return jsonify({
        'passed': passed,
        'score': round(score, 2),
        'required_score': quiz.passing_score,
        'correct_answers': correct_count,
        'total_questions': len(questions)
    })

@app.route('/employee/certificate/<int:cert_id>')
@login_required
def view_certificate(cert_id):
    certificate = Certificate.query.get(cert_id)
    
    if not certificate or certificate.user_id != current_user.id:
        return "Certificate not found", 404
    
    return render_template('certificate.html', certificate=certificate)

# ==================== ROUTES - ADMIN ====================

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    total_employees = User.query.filter_by(is_admin=False).count()
    total_modules = TrainingModule.query.count()
    total_attempts = QuizAttempt.query.count()
    
    return render_template('admin_dashboard.html',
                         total_employees=total_employees,
                         total_modules=total_modules,
                         total_attempts=total_attempts)

@app.route('/admin/modules')
@admin_required
def manage_modules():
    modules = TrainingModule.query.all()
    return render_template('manage_modules.html', modules=modules)

@app.route('/api/admin/module', methods=['POST'])
@admin_required
def create_module():
    data = request.json
    module = TrainingModule(
        title=data.get('title'),
        description=data.get('description'),
        content=data.get('content'),
        duration_minutes=data.get('duration_minutes')
    )
    db.session.add(module)
    db.session.commit()
    
    return jsonify({'id': module.id, 'message': 'Module created successfully'})

@app.route('/api/admin/module/<int:module_id>', methods=['PUT', 'DELETE'])
@admin_required
def update_delete_module(module_id):
    module = TrainingModule.query.get(module_id)
    
    if not module:
        return jsonify({'error': 'Module not found'}), 404
    
    if request.method == 'DELETE':
        db.session.delete(module)
        db.session.commit()
        return jsonify({'message': 'Module deleted'})
    
    if request.method == 'PUT':
        data = request.json
        module.title = data.get('title', module.title)
        module.description = data.get('description', module.description)
        module.content = data.get('content', module.content)
        module.duration_minutes = data.get('duration_minutes', module.duration_minutes)
        db.session.commit()
        
        return jsonify({'message': 'Module updated'})

@app.route('/admin/reports')
@admin_required
def reports():
    # Quiz Statistics
    quiz_attempts = QuizAttempt.query.all()
    
    passed_count = sum(1 for attempt in quiz_attempts if attempt.passed)
    failed_count = sum(1 for attempt in quiz_attempts if not attempt.passed)
    
    # Group by quiz
    quiz_stats = {}
    for attempt in quiz_attempts:
        quiz_id = attempt.quiz_id
        if quiz_id not in quiz_stats:
            quiz_stats[quiz_id] = {'attempts': 0, 'passed': 0, 'failed': 0}
        
        quiz_stats[quiz_id]['attempts'] += 1
        if attempt.passed:
            quiz_stats[quiz_id]['passed'] += 1
        else:
            quiz_stats[quiz_id]['failed'] += 1
    
    # Module completion stats
    modules = TrainingModule.query.all()
    module_stats = []
    for module in modules:
        total_enrolled = Enrollment.query.filter_by(module_id=module.id).count()
        completed = Enrollment.query.filter_by(module_id=module.id, is_completed=True).count()
        
        module_stats.append({
            'module': module,
            'total_enrolled': total_enrolled,
            'completed': completed,
            'completion_rate': (completed / total_enrolled * 100) if total_enrolled > 0 else 0
        })
    
    return render_template('reports.html',
                         quiz_stats=quiz_stats,
                         module_stats=module_stats,
                         total_attempts=len(quiz_attempts),
                         total_passed=passed_count,
                         total_failed=failed_count)

@app.route('/api/admin/quiz-report')
@admin_required
def get_quiz_report():
    quiz_id = request.args.get('quiz_id', type=int)
    
    if quiz_id:
        attempts = QuizAttempt.query.filter_by(quiz_id=quiz_id).all()
    else:
        attempts = QuizAttempt.query.all()
    
    report_data = []
    for attempt in attempts:
        report_data.append({
            'employee_name': attempt.user.full_name,
            'employee_email': attempt.user.email,
            'quiz_title': attempt.quiz.title,
            'attempted_at': attempt.attempted_at.strftime('%Y-%m-%d %H:%M:%S'),
            'score': attempt.score,
            'passed': attempt.passed,
            'required_score': attempt.quiz.passing_score
        })
    
    return jsonify(report_data)

@app.route('/admin/employees')
@admin_required
def manage_employees():
    employees = User.query.filter_by(is_admin=False).all()
    return render_template('manage_employees.html', employees=employees)

@app.route('/api/admin/employee', methods=['POST'])
@admin_required
def create_employee():
    data = request.json
    
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    employee = User(
        username=data.get('username'),
        password=generate_password_hash(data.get('password')),
        full_name=data.get('full_name'),
        email=data.get('email'),
        department=data.get('department'),
        is_admin=False
    )
    db.session.add(employee)
    db.session.commit()
    
    return jsonify({'id': employee.id, 'message': 'Employee created successfully'})

@app.route('/admin/settings')
@admin_required
def admin_settings():
    return render_template('admin_settings.html')

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404, error_message='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error_code=500, error_message='Internal server error'), 500

# ==================== DATABASE INITIALIZATION ====================

def init_db():
    """Initialize database with sample data"""
    with app.app_context():
        db.create_all()
        
        # Check if admin exists
        admin = User.query.filter_by(username='itadmin').first()
        if not admin:
            admin = User(
                username='itadmin',
                password=generate_password_hash('Brian1234'),
                full_name='Admin User',
                email='admin@company.com',
                is_admin=True
            )
            db.session.add(admin)
        
        # Check if employee exists
        employee = User.query.filter_by(username='cathy').first()
        if not employee:
            employee = User(
                username='cathy',
                password=generate_password_hash('Catherine@15'),
                full_name='Cathy Employee',
                email='cathy@company.com',
                department='HR',
                is_admin=False
            )
            db.session.add(employee)
        
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
