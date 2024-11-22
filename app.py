import random
import subprocess
from flask import Flask, abort, render_template, request, redirect, url_for
from schemas.schemas import db, Period, Response, Question, Student, PeriodQuestion
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from matching import find_best_match_for_each

app = Flask(__name__, template_folder='templates', static_folder='StaticFile')

# MySQL database URI
dbUser = "root" #!!! Must be updated locally | The username to access your SQL server
dbPass = "Charlotte43" #!!! Must be updated locally | The password to access your SQL server
dbName = "flask2" #!! Must be updated locally | The name of your schema in the database

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
        mQ1 = Question(text="What year are you?", options=", freshman, sophomore, junior, senior, graduate-student", questiontype=1)
        mQ2 = Question(text="What is your major?", options="...", questiontype=1)
        mQ3 = Question(text="Would you prefer a roommate with the same major?", options=", yes, no, doesn't matter", questiontype=1)
        mQ4 = Question(text="How do you feel about sharing personal items?", options=", 1, 2, 3, 4, 5", questiontype=1)
        mQ5 = Question(text="What time would you like to have quiet hours?", options=", 8pm, 10pm, midnight", questiontype=1)
        mQ6 = Question(text="What time do you usually go to sleep?", options=", 8pm-10pm, 10pm-midnight, after-midnight", questiontype=1)
        mQ7 = Question(text="What are your study habits? (Select all that apply)", options=", Study Alone, Late Night Study, Common Areas Study, In Room Study, Background Noise Study", questiontype=1)
        mQ8 = Question(text="What are your hobbies? (Select all that apply)", options=", Sports, Reading, Gaming, Art, Cooking", questiontype=1)
        mQ9 = Question(text="What kind of room climate do you prefer?", options=", cool, warm, moderate", questiontype=1)
        mQ10 = Question(text="How tidy do you like to keep your space?", options=", tidy, messy", questiontype=1)
        mQ11 = Question(text="How do you handle conflict?", options=", confront, avoid", questiontype=1)

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

# Default routing to the index page.
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

#Routing to the survey page.
@app.route('/survey', methods=['GET'])
def survey():
    return render_template('survey.html')

#Routing to post new information to the database.
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

#Route to display all user responses.
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
    # to-do: update this using a text file.
]

#Route to post simulated responses to the database.
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

    #Redirect to the responses page after we are done posting the simulated responses.
    return redirect(url_for('display_responses'))

@app.route('/matching', methods=['GET', 'POST'])
def matching():
    best_matches = {}

    # Handle form submission or button click to trigger matching process
    if request.method == 'POST':
        # Pass the database URL to the matching script
        process = subprocess.Popen( #In order for us to do multiprocessing in a flask app, we need to run the matching script as a completely separete process. 
            ['venv/Scripts/python', 'matching.py', app.config['SQLALCHEMY_DATABASE_URI']], #We pass the virtual environment's python.exe so the matching script can take advantage of our installed modules, and the database URI so it can access the database.
            stdout=subprocess.PIPE, #We pipe the standard output (our matched responses)
            stderr=subprocess.PIPE #And we also pipe the standard error (Our debug statements)
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