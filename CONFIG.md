# Configuration Guide

## Customization Options

### 1. Change Admin/Employee Credentials

Edit `app.py` in the `init_db()` function:

```python
# Admin account
admin = User(
    username='itadmin',
    password=generate_password_hash('Brian1234'),  # Change password here
    full_name='Admin User',
    email='admin@company.com',
    is_admin=True
)

# Employee account
employee = User(
    username='cathy',
    password=generate_password_hash('Catherine@15'),  # Change password here
    full_name='Cathy Employee',
    email='cathy@company.com',
    department='HR',
    is_admin=False
)
```

Then restart the application: `python app.py`

### 2. Change Application Settings

#### Secret Key
```python
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
```

**Important:** Change this to a random string for production.

#### Database Location
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee_training.db'
```

To use a different database:
- MySQL: `'mysql+pymysql://user:password@localhost/dbname'`
- PostgreSQL: `'postgresql://user:password@localhost/dbname'`
- (Install required driver: `pip install pymysql` or `pip install psycopg2`)

#### Debug Mode
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

- `debug=False` for production
- `host='localhost'` to restrict to local only
- `port=5000` change to any available port

### 3. Customize Theme Colors

Edit `static/css/style.css`:

```css
/* Primary Colors */
/* Change from #667eea to your color */
.navbar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.btn-primary {
    background: #667eea;
}

.dashboard-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

Common color codes:
- Professional Blue: `#003366`
- Modern Purple: `#667eea`
- Corporate Green: `#27ae60`
- Tech Black: `#1a1a1a`

### 4. Add New Quiz Question Types

Edit `app.py` in the `take_quiz` template:

```python
# Add new question type
elif question.question_type == 'short_answer':
    # Handle short answer validation
    pass

elif question.question_type == 'matching':
    # Handle matching questions
    pass
```

### 5. Change Quiz Passing Score

Default: 70%

**Per Quiz:** Edit in Admin UI when creating quiz
**Global Default:** Edit in `app.py`:

```python
class Quiz(db.Model):
    passing_score = db.Column(db.Integer, default=75)  # Change 75 to desired value
```

### 6. Add Email Notifications

Install Flask-Mail:
```bash
pip install Flask-Mail
```

Add to `app.py`:
```python
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-password'

mail = Mail(app)

# Send email on certificate generation
def send_certificate_email(employee_email, module_name):
    msg = Message(
        'Certificate Earned!',
        sender='noreply@training.com',
        recipients=[employee_email]
    )
    msg.body = f'Congratulations! You have completed {module_name}'
    mail.send(msg)
```

### 7. Customize Certificate Template

Edit `templates/certificate.html`:

```html
<!-- Change certificate styling -->
.certificate-border {
    border: 5px solid #1a5490;  /* Change border color */
    background: linear-gradient(135deg, #fffef7 0%, #fffff0 100%);
}

.certificate-header h1 {
    color: #1a5490;  /* Change text color */
    font-size: 48px;
}
```

### 8. Add Company Logo

1. Place logo in `static/` folder (e.g., `static/logo.png`)
2. Update `templates/base.html`:

```html
<nav class="navbar">
    <div class="navbar-container">
        <img src="{{ url_for('static', filename='logo.png') }}" alt="Logo" class="navbar-logo">
        <div class="logo">Employee Training System</div>
```

3. Update `templates/certificate.html`:

```html
<div class="certificate-header">
    <img src="static/logo.png" alt="Company Logo" style="max-width: 100px;">
    <h1>Certificate of Completion</h1>
</div>
```

### 9. Modify Default Employee Department

Edit `templates/manage_employees.html`:

```html
<div class="form-group">
    <label for="empDepartment">Department:</label>
    <select id="empDepartment" name="department">
        <option value="">Select Department</option>
        <option value="HR">Human Resources</option>
        <option value="IT">Information Technology</option>
        <option value="Finance">Finance</option>
        <option value="Sales">Sales</option>
        <option value="Operations">Operations</option>
    </select>
</div>
```

### 10. Add New Admin Features

#### Add System Backup
```python
import shutil
from datetime import datetime

@app.route('/api/admin/backup', methods=['POST'])
@admin_required
def backup_database():
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    backup_file = f'backups/employee_training_{timestamp}.db'
    shutil.copy('employee_training.db', backup_file)
    return jsonify({'message': 'Backup created', 'file': backup_file})
```

#### Add Data Export
```python
@app.route('/api/admin/export-employees', methods=['GET'])
@admin_required
def export_employees():
    employees = User.query.filter_by(is_admin=False).all()
    data = [{
        'id': e.id,
        'name': e.full_name,
        'username': e.username,
        'email': e.email,
        'department': e.department
    } for e in employees]
    return jsonify(data)
```

### 11. Customize Report Filters

Add to `templates/reports.html`:

```html
<div class="report-filters">
    <label>Filter by Department:</label>
    <select id="departmentFilter">
        <option value="">All</option>
        <option value="IT">IT</option>
        <option value="HR">HR</option>
    </select>
    
    <label>Filter by Module:</label>
    <select id="moduleFilter">
        <option value="">All</option>
        {% for module in modules %}
        <option value="{{ module.id }}">{{ module.title }}</option>
        {% endfor %}
    </select>
</div>
```

### 12. Enable HTTPS

For production deployment with SSL:

```python
if __name__ == '__main__':
    app.run(
        debug=False,
        host='0.0.0.0',
        port=5000,
        ssl_context='adhoc'  # Requires pyopenssl
    )
```

Or use environment variables:
```python
import os
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
```

### 13. Add Database Connection Pooling

For MySQL/PostgreSQL:

```python
from sqlalchemy.pool import QueuePool

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'poolclass': QueuePool,
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
```

### 14. Enable Logging

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### 15. Rate Limiting

Install Flask-Limiter:
```bash
pip install Flask-Limiter
```

Add to `app.py`:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Login logic
    pass
```

---

## Environment Variables

Create `.env` file:
```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///employee_training.db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-password
```

Load in `app.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
```

---

## Production Deployment

### Using Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Nginx:
```nginx
upstream flask_app {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://flask_app;
    }
}
```

---

## Troubleshooting Configuration

### Issue: Database not found
```python
# Use absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////full/path/to/employee_training.db'
```

### Issue: Static files not loading
```python
# Check static folder path
app.static_folder = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static')
```

### Issue: Port already in use
```bash
# Find and kill process
lsof -i :5000
kill -9 <PID>

# Or use different port
python app.py  # In browser: localhost:5001
```

---

For more information, see README.md and DEPLOYMENT.md
