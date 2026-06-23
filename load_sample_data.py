"""
Sample data loader for testing the Employee Training System
Run this script to add sample modules and quizzes to the database
"""

from app import app, db, TrainingModule, Quiz, QuizQuestion, User

def load_sample_data():
    """Load sample training modules and quizzes"""
    
    with app.app_context():
        # Check if modules already exist
        if TrainingModule.query.first():
            print("Sample data already exists!")
            return
        
        # Create sample modules
        modules_data = [
            {
                'title': 'Python Basics',
                'description': 'Learn the fundamentals of Python programming',
                'content': '''
                <h3>Python Basics Course</h3>
                <p>This module covers:</p>
                <ul>
                    <li>Variables and Data Types</li>
                    <li>Control Structures (if, for, while)</li>
                    <li>Functions and Modules</li>
                    <li>Basic File I/O</li>
                    <li>Error Handling</li>
                </ul>
                <p>By the end of this module, you will be able to write basic Python programs.</p>
                ''',
                'duration_minutes': 120
            },
            {
                'title': 'Web Development Basics',
                'description': 'Introduction to web development with HTML, CSS, and JavaScript',
                'content': '''
                <h3>Web Development Course</h3>
                <p>This module covers:</p>
                <ul>
                    <li>HTML Structure and Semantics</li>
                    <li>CSS Styling and Layouts</li>
                    <li>JavaScript Basics</li>
                    <li>Responsive Design</li>
                    <li>Web Standards and Best Practices</li>
                </ul>
                <p>Learn to build modern, responsive web applications.</p>
                ''',
                'duration_minutes': 150
            },
            {
                'title': 'Database Management',
                'description': 'Learn SQL and database design principles',
                'content': '''
                <h3>Database Management Course</h3>
                <p>This module covers:</p>
                <ul>
                    <li>Relational Database Concepts</li>
                    <li>SQL Queries and Manipulation</li>
                    <li>Database Design and Normalization</li>
                    <li>Indexes and Performance</li>
                    <li>Backup and Recovery</li>
                </ul>
                <p>Master the fundamentals of database management.</p>
                ''',
                'duration_minutes': 140
            },
            {
                'title': 'Cybersecurity Fundamentals',
                'description': 'Essential cybersecurity concepts and practices',
                'content': '''
                <h3>Cybersecurity Fundamentals Course</h3>
                <p>This module covers:</p>
                <ul>
                    <li>Common Security Threats</li>
                    <li>Password Security</li>
                    <li>Encryption Basics</li>
                    <li>Safe Browsing Practices</li>
                    <li>Incident Response</li>
                </ul>
                <p>Protect yourself and your organization from security threats.</p>
                ''',
                'duration_minutes': 90
            }
        ]
        
        # Add modules and quizzes
        for module_data in modules_data:
            module = TrainingModule(**module_data)
            db.session.add(module)
            db.session.flush()  # Flush to get the module ID
            
            # Create quiz for each module
            quiz = Quiz(
                module_id=module.id,
                title=f"{module.title} Quiz",
                passing_score=70
            )
            db.session.add(quiz)
            db.session.flush()
            
            # Add sample questions for each quiz
            questions = get_sample_questions(module.title)
            for q in questions:
                question = QuizQuestion(
                    quiz_id=quiz.id,
                    question_text=q['text'],
                    question_type=q['type'],
                    options=q['options'],
                    correct_answer=q['correct']
                )
                db.session.add(question)
        
        db.session.commit()
        print("✓ Sample data loaded successfully!")
        print(f"✓ Created {len(modules_data)} modules with quizzes")

def get_sample_questions(module_title):
    """Get sample questions for each module"""
    
    questions_map = {
        'Python Basics': [
            {
                'text': 'What is the correct way to create a list in Python?',
                'type': 'multiple_choice',
                'options': 'my_list = []|my_list = {}|my_list = ()|my_list = <>',
                'correct': 'my_list = []'
            },
            {
                'text': 'Python is a compiled language.',
                'type': 'true_false',
                'options': 'True|False',
                'correct': 'False'
            },
            {
                'text': 'Which keyword is used to create a function in Python?',
                'type': 'multiple_choice',
                'options': 'def|function|func|define',
                'correct': 'def'
            },
        ],
        'Web Development Basics': [
            {
                'text': 'What does HTML stand for?',
                'type': 'multiple_choice',
                'options': 'Hyper Text Markup Language|High Tech Modern Language|Home Tool Markup Language|Hyperlinks and Text Markup Language',
                'correct': 'Hyper Text Markup Language'
            },
            {
                'text': 'CSS is used to define the structure of web pages.',
                'type': 'true_false',
                'options': 'True|False',
                'correct': 'False'
            },
            {
                'text': 'Which tag is used to create a hyperlink in HTML?',
                'type': 'multiple_choice',
                'options': '<link>|<a>|<href>|<url>',
                'correct': '<a>'
            },
        ],
        'Database Management': [
            {
                'text': 'What does SQL stand for?',
                'type': 'multiple_choice',
                'options': 'Structured Query Language|Standard Question Language|Structured Question Logic|Simple Query Logic',
                'correct': 'Structured Query Language'
            },
            {
                'text': 'A primary key can have NULL values.',
                'type': 'true_false',
                'options': 'True|False',
                'correct': 'False'
            },
            {
                'text': 'Which SQL command is used to retrieve data?',
                'type': 'multiple_choice',
                'options': 'SELECT|RETRIEVE|FETCH|GET',
                'correct': 'SELECT'
            },
        ],
        'Cybersecurity Fundamentals': [
            {
                'text': 'What is the most common form of cyber attack?',
                'type': 'multiple_choice',
                'options': 'Phishing|DDoS|Malware|SQL Injection',
                'correct': 'Phishing'
            },
            {
                'text': 'Using the same password for all accounts is a good security practice.',
                'type': 'true_false',
                'options': 'True|False',
                'correct': 'False'
            },
            {
                'text': 'What does MFA stand for?',
                'type': 'multiple_choice',
                'options': 'Multi-Factor Authentication|Multi-File Access|Modern Firewall Access|Maximum File Authorization',
                'correct': 'Multi-Factor Authentication'
            },
        ]
    }
    
    return questions_map.get(module_title, [])

if __name__ == '__main__':
    load_sample_data()
