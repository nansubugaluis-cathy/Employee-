# Quick Start Guide - Employee Training System

## Step 1: Install Dependencies

```bash
cd /workspaces/Employee-
pip install -r requirements.txt
```

## Step 2: Initialize the System

```bash
python app.py
```

This will:
- Create the SQLite database (`employee_training.db`)
- Set up all tables
- Add default admin and employee accounts

## Step 3: Load Sample Data (Optional)

To add sample training modules and quizzes:

```bash
python load_sample_data.py
```

## Step 4: Access the Application

Open your browser and go to: `http://localhost:5000`

## Step 5: Login

### Admin Access:
- URL: `http://localhost:5000/login`
- Username: `itadmin`
- Password: `Brian1234`

### Employee Access:
- URL: `http://localhost:5000/login`
- Username: `cathy`
- Password: `Catherine@15`

## Admin Functions

After logging in as admin, you can:

1. **Create Training Modules**
   - Go to "Modules" → "Add New Module"
   - Enter module details (title, description, content, duration)
   - System automatically creates a quiz for each module

2. **Add Employees**
   - Go to "Employees" → "Add New Employee"
   - Enter employee information
   - System creates login credentials

3. **Create Quizzes**
   - Quizzes are auto-created with modules
   - Add questions through the database or directly

4. **View Reports**
   - Go to "Reports"
   - See quiz statistics:
     - Total attempts
     - Pass/fail counts
     - Completion rates
     - Employee performance
   - Export data to CSV

5. **Monitor System**
   - Go to "Settings"
   - Check system status
   - Validate connections
   - Perform diagnostics

## Employee Functions

After logging in as employee, you can:

1. **View Dashboard**
   - See enrolled modules
   - Track completion progress
   - View earned certificates

2. **Complete Modules**
   - Click on a module to read content
   - Click "Take Quiz" to test knowledge

3. **Take Quizzes**
   - Answer multiple-choice or true/false questions
   - Get instant score after submission
   - See if you passed or failed

4. **Earn Certificates**
   - Certificate automatically generated upon passing
   - View and download certificates from dashboard
   - Print certificates for records

## Features

### ✅ Training Modules
- Create and manage training content
- Track enrollment and completion
- Set module duration

### ✅ Quizzes
- Multiple-choice and true/false questions
- Automatic scoring
- Configurable passing scores
- Unlimited attempts

### ✅ Certificates
- Auto-generated upon quiz completion
- Unique certificate numbers
- Printable format
- Completion tracking

### ✅ Reports & Analytics
- Quiz attempt statistics
- Pass/fail breakdown by employee
- Module completion rates
- CSV export capability

### ✅ System Reliability
- Database validation
- Connection monitoring
- Error handling
- Real-time status checks

## Troubleshooting

### Application won't start
- Ensure Python 3.7+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Check if port 5000 is available

### Can't login
- Verify username and password
- Check database is initialized
- Try the default credentials

### No modules available
- Run the sample data loader: `python load_sample_data.py`
- Or create modules through admin interface

### Reports not loading
- Check database connection
- Ensure quiz attempts exist
- Clear browser cache

## File Structure

```
Employee-/
├── app.py                          # Main Flask application
├── load_sample_data.py            # Sample data loader
├── requirements.txt               # Python dependencies
├── employee_training.db           # SQLite database (auto-created)
├── templates/                     # HTML templates
│   ├── base.html                 # Base template
│   ├── login.html                # Login page
│   ├── admin_dashboard.html      # Admin dashboard
│   ├── employee_dashboard.html   # Employee dashboard
│   ├── manage_modules.html       # Module management
│   ├── manage_employees.html     # Employee management
│   ├── reports.html              # Reports and analytics
│   ├── take_quiz.html            # Quiz interface
│   ├── view_module.html          # Module view
│   ├── certificate.html          # Certificate display
│   ├── admin_settings.html       # Admin settings
│   ├── error.html                # Error pages
│   └── README.md                 # Documentation
└── static/                        # Static files
    ├── css/
    │   └── style.css             # Stylesheet
    └── js/
        └── main.js               # JavaScript utilities
```

## Next Steps

1. Test with sample data
2. Create your own training modules
3. Add employees
4. Monitor quiz completion and performance
5. Export reports for analysis

## Support

For issues or questions, refer to the main README.md file for detailed documentation.

---

**Version:** 1.0
**Last Updated:** 2024