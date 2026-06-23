# Employee Training System

A comprehensive web-based platform for managing employee training modules, quizzes, and certificates.

## Features

### For Employees
- ✅ Enroll in training modules
- ✅ Complete interactive modules
- ✅ Take quizzes with automatic scoring
- ✅ Earn certificates upon module completion
- ✅ View personal dashboard with progress
- ✅ Download and view certificates

### For Administrators
- ✅ Create and manage training modules
- ✅ Create and manage quizzes with questions
- ✅ Manage employee accounts
- ✅ View comprehensive reports:
  - Number of employees who attempted quizzes
  - Pass/fail statistics per quiz
  - Module completion rates
  - Export data to CSV
- ✅ System validation and monitoring
- ✅ Database management and backup
- ✅ Real-time system status

## Technology Stack
- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript
- **Authentication:** Flask-Login with password hashing

## Installation

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Setup Instructions

1. **Clone or download the repository:**
```bash
cd /workspaces/Employee-
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Initialize the database:**
```bash
python app.py
```
This will create the SQLite database and add default admin and employee accounts.

4. **Run the application:**
```bash
python app.py
```

The application will start at `http://localhost:5000`

## Default Login Credentials

### Administrator Account
- **Username:** `itadmin`
- **Password:** `Brian1234`

### Employee Account
- **Username:** `cathy`
- **Password:** `Catherine@15`

## Usage

### Admin Dashboard
1. Login with admin credentials
2. Access the admin dashboard at `/admin/dashboard`
3. Navigate to:
   - **Modules:** Create and manage training modules
   - **Employees:** Add and manage employee accounts
   - **Reports:** View comprehensive training statistics and analytics
   - **Settings:** Monitor system status and perform maintenance

### Employee Dashboard
1. Login with employee credentials
2. Access the employee dashboard
3. View enrolled modules
4. Complete modules and take quizzes
5. Download certificates after passing quizzes

## System Features

### Module Management
- Create training modules with descriptions and content
- Set module duration
- Automatically track enrollment and completion

### Quiz System
- Create multiple-choice and true/false questions
- Set passing score requirements
- Automatic scoring and result calculation
- Question randomization support

### Certificate Generation
- Automatic certificate creation upon quiz completion
- Unique certificate numbers
- Printable certificate format
- Certificate tracking and viewing

### Reports & Analytics
- Quiz attempt tracking
- Pass/fail statistics
- Module completion rates
- Employee performance metrics
- CSV export for data analysis

### System Validation
- Database integrity checks
- Connection monitoring
- Real-time system status
- Validation logs

## API Endpoints

### Authentication
- `GET /` - Redirect to appropriate dashboard
- `POST /login` - User login
- `GET /logout` - User logout

### Employee Routes
- `GET /employee/dashboard` - Employee dashboard
- `GET /employee/module/<id>` - View training module
- `GET /employee/quiz/<id>` - Take quiz
- `POST /api/quiz/<id>/submit` - Submit quiz answers
- `GET /employee/certificate/<id>` - View certificate

### Admin Routes
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/modules` - Manage modules
- `POST /api/admin/module` - Create module
- `PUT /api/admin/module/<id>` - Update module
- `DELETE /api/admin/module/<id>` - Delete module
- `GET /admin/employees` - Manage employees
- `POST /api/admin/employee` - Add employee
- `GET /admin/reports` - View reports
- `GET /api/admin/quiz-report` - Get detailed quiz report
- `GET /admin/settings` - System settings

## Database Schema

### Users Table
- Stores user information (admin and employees)
- Manages authentication credentials
- Tracks user roles and permissions

### Training Modules Table
- Stores module information
- Tracks module content and metadata
- Manages enrollment relationships

### Enrollments Table
- Tracks employee enrollment in modules
- Records completion status
- Maintains enrollment history

### Quizzes Table
- Stores quiz information linked to modules
- Sets passing scores
- Manages quiz questions

### Quiz Attempts Table
- Records employee quiz attempts
- Stores scores and pass/fail status
- Maintains attempt history

### Certificates Table
- Stores issued certificates
- Links certificates to users and modules
- Tracks certificate numbers and dates

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- User role validation (admin/employee)
- CSRF protection ready
- SQL injection prevention via ORM

## System Validation & Reliability

The system includes:
- ✅ Database connection validation
- ✅ User authentication verification
- ✅ Input validation on all forms
- ✅ Error handling and logging
- ✅ Real-time system status monitoring
- ✅ Backup capabilities
- ✅ Data integrity checks

## Support & Maintenance

### System Check
Visit `/admin/settings` to:
- Check system status
- Validate all connections
- Run diagnostics
- Backup database
- Download logs

### Troubleshooting
- Check database connection
- Verify user permissions
- Review error logs
- Validate all required fields in forms

## License
This system is proprietary and confidential.

## Version
v1.0 - Initial Release (2024)
