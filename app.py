import os
import random
import subprocess
import sys
from flask import Flask, abort, render_template, request, redirect, url_for
from schemas.schemas import db, Period, Response, Question, Student, PeriodQuestion
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from matching import find_best_match_for_each

app = Flask(__name__, template_folder='templates', static_folder='StaticFile')

# MySQL database URI

dbUser = "root" #!!! Must be updated locally | The username to access your SQL server
dbPass = "12345" #!!! Must be updated locally | The password to access your SQL server
dbName = "roommate" #!! Must be updated locally | The name of your schema in the database

def ensure_schema_exists(): #Ensures that the schema exists on the database. If it does not exist, it will make it. Uses dbName as the name.
    temp_engine = create_engine(f'mysql://{dbUser}:{dbPass}@127.0.0.1:3306') #Create a temp SQL engine to create the schema.
    with temp_engine.connect() as conn: #Use the temp engine...
         conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {dbName}")) #Create the schema if it doesn't exist, using dbName as the name.
         conn.execute(text(f"USE {dbName}"))  # Explicitly switch to the schema (In case your database is using a different schema)
    temp_engine.dispose() #Destroy the temp engine after, we'll use SQLAlchemy to manage engines from now on.

ensure_schema_exists() #Run the function.

#Configure the database URI using the username, password, and schema name.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://'+dbUser+':'+dbPass+'@127.0.0.1:3306/'+dbName 

# Disable tracking modifications to save resources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database object
db.init_app(app)  

#Perform database setup 
with app.app_context():
        db.drop_all()  # Drops all tables
        db.create_all() # Re-creates tables from schema file

        # Adding the Period
        mPeriod = Period(periodName="Fall 2024", numDoubles=200, numQuads=100)

        # Adding in all 11 Questions, Question type is non functional
        mQ1 = Question(text="What year are you?", options=", freshman, sophomore, junior, senior, graduate-student", caption="Year", questiontype=1)
        mQ2 = Question(text="What is your major?", options="...", caption="Major", questiontype=2)
        mQ3 = Question(text="Would you prefer a roommate with the same major?", options=", yes, no, doesn't matter", caption="Same Major Preference", questiontype=1)
        mQ4 = Question(text="How do you feel about sharing personal items?", subtext="(1 = Not Comfortable, 5 = Very Comfortable)", options=", 1, 2, 3, 4, 5", caption="Room Sharing", questiontype=3)
        mQ5 = Question(text="What time would you like to have quiet hours?", options=", 8pm, 10pm, midnight", caption="Quiet Hours", questiontype=1)
        mQ6 = Question(text="What time do you usually go to sleep?", options=", 8pm-10pm, 10pm-midnight, after-midnight", caption="Preferred Sleep Time", questiontype=1)
        mQ7 = Question(text="What are your study habits?", options=", Study Alone, Late Night Study, Common Areas Study, In Room Study, Background Noise Study", caption="Study Habits", questiontype=4)
        mQ8 = Question(text="What are your hobbies?", options=", Sports, Reading, Gaming, Art, Cooking", caption="Hobbies", questiontype=4)
        mQ9 = Question(text="What kind of room climate do you prefer?", options=", cool, warm, moderate", caption="Preferred Room Climate", questiontype=1)
        mQ10 = Question(text="How tidy do you like to keep your space?", options=", tidy, messy", caption="Cleanliness", questiontype=1)
        mQ11 = Question(text="How do you handle conflict?", options=", confront, avoid",caption="Conflict Resolution Style", questiontype=1)
        mQ12 = Question(text="Are you excited for college?", options=", YES!!!, no",caption="Are you excited", questiontype=1)

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
        mPeriod.periodquestions.append(mQ12)

        db.session.add_all([mPeriod, mQ1, mQ2, mQ3, mQ4, mQ5, mQ6, mQ7, mQ8, mQ9, mQ10, mQ11])
        db.session.commit()

global currentPeriod 
currentPeriod = 1
MAXQUESTIONS = 15

# Default routing to the index page.
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#Routing to the survey page.
@app.route('/survey', methods=['GET'])
def survey():
    # TODO query periodQuestions table with a join with current period
    period = Period().query.get_or_404(currentPeriod)
    all_questions = period.periodquestions
    print("!!!!!! ",currentPeriod)
    return render_template('survey.html', all_questions=all_questions)

#Routing to post new information to the database.
@app.route('/user', methods=['POST'])
def userResponses():
    # Since we have no login atm, I'm just making a new student when we get responses
    mStudent = Student(firstname="test", lastname="test")
    
    # Retrieve form data
    period = Period().query.get_or_404(currentPeriod)
    all_questions = period.periodquestions

    # Ohhh I hate this but its 15 Nones 
    qResponse = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]

    for i in range(len(all_questions)):
        if all_questions[i].questiontype == 4:
            qResponse[i] = ', '.join(request.form.getlist(f'{i+1}'))
        else:
            qResponse[i] = request.form.get(f'{i+1}', '')
    
    print(qResponse)

    # TODO loop through questions to get a response for each
    mResponse = Response(
        q1=qResponse[0],
        q2=qResponse[1],
        q3=qResponse[2],
        q4=qResponse[3],
        q5=qResponse[4],
        q6=qResponse[5],
        q7=qResponse[6], 
        q8=qResponse[7], 
        q9=qResponse[8],
        q10=qResponse[9],
        q11=qResponse[10],
        q12=qResponse[11], 
        q13=qResponse[12],
        q14=qResponse[13],
        q15=qResponse[14]
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

#Route to display all user responses.
@app.route('/responses')
def display_responses():
    # Query all responses from the database, sorted by ID
    all_responses = Response.query.order_by(Response.id).all()
    period = Period().query.get_or_404(currentPeriod)
    all_questions = period.periodquestions
    
    # Pass the responses to the template
    return render_template('responses.html', all_responses=all_responses, all_questions=all_questions)

# List of majors
majors = [
    "Computer science", "Psychology", "Finance", "Health/health care administration/management", 
    "Speech communication and rhetoric", "Biology/biological sciences", "Criminal justice/safety studies", 
    "Marketing/marketing management", "Exercise physiology", "Political science and government", 
    # to-do: update this using a text file.
]

#Route to post simulated responses to the database.
@app.route('/simulate_responses', methods=['POST'])
def simulate_responses():
    num_responses = int(request.form['num_responses'])

    period = Period().query.get_or_404(currentPeriod)
    all_questions = period.periodquestions

    for i in range(num_responses):
        # Simulate a response matching the survey structure
        
        # Ohhh I hate this but its 15 Nones 
        qResponse = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]
        
        for i in range(len(all_questions)):
            # Majors are a special case 
            if all_questions[i].questiontype == 2:
                qResponse[i] = random.choice(majors)
            else:
                options = all_questions[i].options.split(", ")[1:]
                if all_questions[i].questiontype == 4:
                    qResponse[i] = ', '.join(random.sample(options, random.randint(1, 3)))
                else:
                    qResponse[i] = random.choice(options)

        # Insert the response into the database
        response = Response(
            q1=qResponse[0],
            q2=qResponse[1],
            q3=qResponse[2],
            q4=qResponse[3],
            q5=qResponse[4],
            q6=qResponse[5],
            q7=qResponse[6], 
            q8=qResponse[7], 
            q9=qResponse[8],
            q10=qResponse[9],
            q11=qResponse[10],
            q12=qResponse[11], 
            q13=qResponse[12],
            q14=qResponse[13],
            q15=qResponse[14]
        )

        # Simulate a student to tie the response to
        mStudent = Student(firstname="John "+str(i), lastname="Smith "+str(i))
        mStudent.response = response

        db.session.add_all([mStudent, response])
        

    # Commit all changes to the database
    db.session.commit()

    #Redirect to the responses page after we are done posting the simulated responses.
    return redirect(url_for('display_responses'))

@app.route('/matching', methods=['GET', 'POST'])
def matching():
    best_matches = {}

    # Handle form submission or button click to trigger matching process
    if request.method == 'POST':
        # Pass the database URL to the matching script
        # Detect the correct path for the virtual environment's Python executable
        
        if sys.platform == 'win32':  # For Windows
            python_executable = os.path.join('venv', 'Scripts', 'python.exe')
        else:  # For macOS/Linux
            python_executable = os.path.join('venv', 'bin', 'python')

        # Ensure the matching script is being executed with the correct Python executable
        process = subprocess.Popen(
            [python_executable, 'matching.py', app.config['SQLALCHEMY_DATABASE_URI']], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        
        # Capture the output from the matching process
        stdout, stderr = process.communicate()

        # Log debug statements via stderr
        if stderr:
            print(f"Matching process debug log: {stderr.decode()}")

        # If there's output, parse it and prepare best matches
        if stdout:
            best_matches = parse_matching_results(stdout.decode())

        # Redirect back to the matching page after completing the process
        all_responses = Response.query.all()
        return render_template('matching.html', all_responses=all_responses, best_matches=best_matches)

    # Render the matching page with best matches (if any)
    all_responses = Response.query.all()
    return render_template('matching.html', all_responses=all_responses, best_matches=best_matches)


def editResponse(responseID, questionNumber, newValue):
    mResponse = Response.query.get_or_404(responseID)
    match questionNumber:
        case 1:
            mResponse.q1 = newValue
        case 2:
            mResponse.q2 = newValue
        case 3:
            mResponse.q3 = newValue
        case 4:
            mResponse.q4 = newValue
        case 5:
            mResponse.q5 = newValue
        case 6:
            mResponse.q6 = newValue
        case 7:
            mResponse.q7 = newValue
        case 8:
            mResponse.q8 = newValue
        case 9:
            mResponse.q9 = newValue
        case 10:
            mResponse.q10 = newValue
        case 11:
            mResponse.q11 = newValue
        case 12:
            mResponse.q12 = newValue
        case 13:
            mResponse.q13 = newValue
        case 14:
            mResponse.q14 = newValue
        case 15:
            mResponse.q15 = newValue
        case _:
            print("Error: Only 15 questions allowed.")

    db.session.commit()

def nullResponse(responseID, questionNumber):
    mResponse = Response.query.get_or_404(responseID)
    match questionNumber:
        case 1:
            mResponse.q1 = None
        case 2:
            mResponse.q2 = None
        case 3:
            mResponse.q3 = None
        case 4:
            mResponse.q4 = None
        case 5:
            mResponse.q5 = None
        case 6:
            mResponse.q6 = None
        case 7:
            mResponse.q7 = None
        case 8:
            mResponse.q8 = None
        case 9:
            mResponse.q9 = None
        case 10:
            mResponse.q10 = None
        case 11:
            mResponse.q11 = None
        case 12:
            mResponse.q12 = None
        case 13:
            mResponse.q13 = None
        case 14:
            mResponse.q14 = None
        case 15:
            mResponse.q15 = None
        case _:
            print("Error: Only 15 questions allowed.")

    db.session.commit()

# GET route for form making new questions
@app.route('/new/question', methods=['GET'])
def question():
    periods = Period().query.all()
    return render_template('newquestion.html', periods=periods, MAXQUESTIONS = MAXQUESTIONS)

# POST route for making new questions
@app.route('/new/question', methods=['POST'])
def createQuestion():
    qText = request.form.get('text', '')
    qOptions = ', '+request.form.get('options')
    qCaption = request.form.get('caption', '')
    qSubtext = request.form.get('subtext', None)
    qType = int(request.form.get('questionType', ''))
    qPeriodID = int(request.form.get('periodID', ''))
    print(qOptions)
    mQuestion = Question(text=qText, subtext=qSubtext, options=qOptions, caption=qCaption, questiontype=qType)
    
    mPeriod = Period().query.get_or_404(qPeriodID)

    mPeriod.periodquestions.append(mQuestion)
    db.session.add(mQuestion)
    db.session.commit()

    return redirect(url_for('admin'))

# GET route for form making new periods of time
@app.route('/new/period', methods=['GET'])
def period():
    questions = Question().query.all()
    return render_template('newperiod.html', questions=questions, MAXQUESTIONS = MAXQUESTIONS)

# POST route for making new periods of time
@app.route('/new/period', methods=['POST'])
def createPeriod():
    periodName = request.form.get('pName', '')
    numDouble = int(request.form.get('numDoubles', ''))
    numQuads = int(request.form.get('numQuads', ''))

    mPeriod = Period(periodName=periodName, numDoubles=numDouble, numQuads=numQuads)

    questions = request.form.getlist('questions')
    
    for i in range(len(questions)):
        if i < 15:
            mQ = Question.query.get_or_404( int(questions[i]) )
            mPeriod.periodquestions.append(mQ)

    db.session.add(mPeriod)
    db.session.commit()

    return redirect(url_for('admin'))

# POST route for updating current period
@app.route('/update/period', methods=['POST'])
def updatePeriod():
    periodID = int(request.form.get('pID', 1))
    global currentPeriod 
    currentPeriod= periodID

    return redirect(url_for('admin'))


def parse_matching_results(output): #Since the matching script returns a string, we need to parse it into a dictonary we can use to render the HTML.
    best_matches = {}
    lines = output.splitlines()

    for line in lines:
        if line.startswith("Response"):
            try:
                # Example line: "Response 1 best match: (203, 7)"
                # Split based on 'best match: ' to separate the response info from the match data
                response_info, match_str = line.split("best match: ")

                # Extract the response_id from the response_info
                response_id = int(response_info.split()[1])  # Extracts the number after "Response"

                # Parse the match_str which is in the format "(match_id, likeness_score)"
                match_str = match_str.strip('()')  # Remove the parentheses
                match_id, likeness_score = map(int, match_str.split(','))  # Convert the two values to integers

                # Store the match in the dictionary
                best_matches[response_id] = (match_id, likeness_score)

            except Exception as e:
                print(f"Error processing line: {line}")
                print(f"Error: {str(e)}")
    return best_matches


@app.route('/admin')
def admin():
    return render_template('adminindex.html')

#Runs the app with debug mode.
if __name__ == "__main__": 
    app.run(debug=True)
