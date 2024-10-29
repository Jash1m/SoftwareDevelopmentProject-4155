import random
# Import necessary libraries from Flask and SQLAlchemy
from flask import Flask, abort, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.sql import text


app = Flask(__name__, template_folder='templates', static_folder='StaticFile')

# MySQL database URI
dbUser = "..." #!!! Must be updated locally
dbPass = "..." #!!! Must be updated locally
dbConnect = "..." #!! Must be updated locally
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+dbUser+':'+dbPass+'@127.0.0.1:3306/'+dbConnect

# Disable tracking modifications to save resources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database object
db = SQLAlchemy(app)

PeriodQuestion = db.Table(
    'periodquestion',
    db.Column('period_id', db.Integer, db.ForeignKey('periods.id')),
    db.Column('question_id', db.Integer, db.ForeignKey('questions.id')),
    
    db.PrimaryKeyConstraint('period_id', 'question_id')
)

'''
Pair = db.Table(
    'pairs',
    db.Column('student_id_1', db.Integer, db.ForeignKey('students.id')),
    db.Column('student_id_2', db.Integer, db.ForeignKey('students.id')),
    db.Column('period_id', db.Integer, db.ForeignKey('periods.id')),

    db.PrimaryKeyConstraint('student_id_1', 'student_id_2', 'period_id')
)

Quad = db.Table(
    'quads',
    db.Column('student_id_1', db.Integer, db.ForeignKey('students.id')),
    db.Column('student_id_2', db.Integer, db.ForeignKey('students.id')),
    db.Column('student_id_3', db.Integer, db.ForeignKey('students.id')),
    db.Column('student_id_4', db.Integer, db.ForeignKey('students.id')),
    db.Column('period_id', db.Integer, db.ForeignKey('periods.id')),

    db.PrimaryKeyConstraint('student_id_1', 'student_id_2', 'student_id_3', 'student_id_4', 'period_id')
)
'''
class Period(db.Model):
    __tablename__ = 'periods'
    
    # Primary key for identifying each period ex. Spring 2024
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    periodName = db.Column(db.String(30), nullable=False)
    numDoubles = db.Column(db.Integer, nullable=False)
    numQuads = db.Column(db.Integer, nullable=False)

    periodquestions = db.relationship('Question', secondary=PeriodQuestion, backref='questionperiods')
    
class Response(db.Model):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    q1 = db.Column(db.String(255), nullable=False, default="freshman")
    q2 = db.Column(db.String(255), nullable=False, default="default")
    q3 = db.Column(db.String(255), nullable=False, default="default")
    q4 = db.Column(db.String(255), nullable=False, default="default")
    q5 = db.Column(db.String(255), nullable=False, default="default")
    q6 = db.Column(db.String(255), nullable=False, default="default")
    q6 = db.Column(db.String(255), nullable=False, default="default")
    q7 = db.Column(db.String(255), nullable=False, default="default")
    q8 = db.Column(db.String(255), nullable=False, default="default")
    q9 = db.Column(db.String(255), nullable=False, default="default")
    q10 = db.Column(db.String(255), nullable=False, default="default")
    q11 = db.Column(db.String(255), nullable=False, default="default")


class Question(db.Model):
    __tablename__ = 'questions'
    
    # Primary key for identifying each question
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(255), nullable=False)
    options = db.Column(db.String(255), nullable=False)
    questiontype = db.Column(db.Integer, nullable=False)

class Student(db.Model):
    __tablename__ = 'students'
    
    # Primary key for identifying each student
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    placed = db.Column(db.Boolean, default=False)

    response = db.relationship('Response', uselist=False, backref='student')
    

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/survey', methods=['GET'])
def survey():
    return render_template('survey.html')


@app.route('/user', methods=['POST'])
def userResponses():
    # Since we have no login atm, I'm just making a new student when we get responses
    #i = i+1
    mStudent = Student(firstname="test", lastname="test")
    
    # Retrieve form data
    mResponse = Response(
        q1=request.form.get('year', ''),
        q2=request.form.get('major', ''),
        q3=request.form.get('same-major', ''),
        q4=request.form.get('share', ''),
        q5=request.form.get('quiet-hours', ''),
        q6=request.form.get('sleep-time', ''),
        q7=', '.join(request.form.getlist('study-habits')),  # Convert list to string
        q8=', '.join(request.form.getlist('hobbies')),       # Convert list to string
        q9=request.form.get('room-climate', ''),
        q10=request.form.get('tidy', ''),
        q11=request.form.get('conflict', '')
    )
    mStudent.response = mResponse

    db.session.add_all([mStudent, mResponse])
    
    # Store the user response in the database
    #db.session.add(responses)

    db.session.commit()  # Commit the session to save changes
    print("Incoming Data!!!! It's WORKING!!!")
    print(mStudent.response)  # Print the response for debugging

    # Redirect to a confirmation or thank you page after submission
    return redirect(url_for('index'))

@app.route('/responses')
def display_responses():
    # Query all responses from the database, sorted by ID
    all_responses = Response.query.order_by(Response.id).all()
    
    # Pass the responses to the template
    return render_template('responses.html', all_responses=all_responses)

# List of majors
majors = [
    "Computer science", "Psychology", "Finance", "Health/health care administration/management", 
    "Speech communication and rhetoric", "Biology/biological sciences", "Criminal justice/safety studies", 
    "Marketing/marketing management", "Exercise physiology", "Political science and government", 
    # to-do: update this dynamically
]

# Simulate responses route with progress
@app.route('/simulate_responses', methods=['POST'])
def simulate_responses():
    num_responses = int(request.form['num_responses'])
    responses = []  # This will store the generated responses

    for i in range(num_responses):
        # Simulate a response matching the survey structure
        new_response = {
            'q1': random.choice(['freshman', 'sophomore', 'junior', 'senior', 'graduate-student']),
            'q2': random.choice(majors),
            'q3': random.choice(['yes', 'no', "doesn't matter"]),
            'q4': str(random.randint(1, 5)),
            'q5': random.choice(['8pm', '10pm', 'midnight']),
            'q6': random.choice(['8pm-10pm', '10pm-midnight', 'after-midnight']),
            'q7': ', '.join(random.sample([
                "Quiet Study", "Study Alone", "Late Night Study", 
                "Common Areas Study", "In Room Study", "Background Noise Study"], random.randint(1, 3))),
            'q8': ', '.join(random.sample([
                "Sports", "Reading", "Gaming", "Art", "Cooking"], random.randint(1, 3))),
            'q9': random.choice(['cool', 'warm', 'moderate']),
            'q10': random.choice(['tidy', 'messy']),
            'q11': random.choice(['confront', 'avoid'])
        }
        
        # Insert the response into the database
        response = Response(
            q1=new_response['q1'],
            q2=new_response['q2'],
            q3=new_response['q3'],
            q4=new_response['q4'],
            q5=new_response['q5'],
            q6=new_response['q6'],
            q7=new_response['q7'],
            q8=new_response['q8'],
            q9=new_response['q9'],
            q10=new_response['q10'],
            q11=new_response['q11']
        )

        # Simulate a student to tie the response to
        mStudent = Student(firstname="John "+str(i), lastname="Smith "+str(i))
        mStudent.response = response

        db.session.add_all([mStudent, response])
        
        # Add to the list for progress tracking
        responses.append(new_response)

    # Commit all changes to the database
    db.session.commit()

    return redirect(url_for('display_responses'))



if __name__ == "__main__": 
    app.run(debug=True)

    with app.app_context():
        db.drop_all()  # Drops all tables
        db.create_all()  # Recreates all tables according to your models

        # Adding the Period
        mPeriod = Period(periodName="Fall 2024", numDoubles=200, numQuads=100)

        # Adding in all 11 Questions
        mQ1 = Question(text="text", options="text", questiontype=1)
        mQ2 = Question(text="text", options="text", questiontype=1)
        mQ3 = Question(text="text", options="text", questiontype=1)
        mQ4 = Question(text="text", options="text", questiontype=1)
        mQ5 = Question(text="text", options="text", questiontype=1)
        mQ6 = Question(text="text", options="text", questiontype=1)
        mQ7 = Question(text="text", options="text", questiontype=1)
        mQ8 = Question(text="text", options="text", questiontype=1)
        mQ9 = Question(text="text", options="text", questiontype=1)
        mQ10 = Question(text="text", options="text", questiontype=1)
        mQ11 = Question(text="text", options="text", questiontype=1)

        # Associating Questions
        mPeriod.periodquestions.append(mQ1)
        mPeriod.periodquestions.append(mQ2)
        mPeriod.periodquestions.append(mQ3)
        mPeriod.periodquestions.append(mQ4)
        mPeriod.periodquestions.append(mQ5)
        mPeriod.periodquestions.append(mQ6)
        mPeriod.periodquestions.append(mQ7)
        mPeriod.periodquestions.append(mQ8)
        mPeriod.periodquestions.append(mQ9)
        mPeriod.periodquestions.append(mQ10)
        mPeriod.periodquestions.append(mQ11)

        db.session.add_all([mPeriod, mQ1, mQ2, mQ3, mQ4, mQ5, mQ6, mQ7, mQ8, mQ9, mQ10, mQ11])
        db.session.commit()

        for i in mPeriod.periodquestions:
            print(i)
