# Import necessary libraries from Flask and SQLAlchemy
from flask import Flask, abort, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder='templates', static_folder='StaticFile')

# SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Disable tracking modifications to save resources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database object
db = SQLAlchemy(app)

# Defined a 'Response' database table model
class Response(db.Model):
    __tablename__ = 'responses'
    
    # Primary key for identifying each user
    id = db.Column(db.Integer, primary_key=True)
    
    # Survey response placeholders for 11 questions, stored as strings
    q1 = db.Column(db.String, nullable=False)
    q2 = db.Column(db.String, nullable=False)
    q3 = db.Column(db.String, nullable=False)
    q4 = db.Column(db.String, nullable=False)
    q5 = db.Column(db.String, nullable=False)
    q6 = db.Column(db.String, nullable=False)
    q7 = db.Column(db.String, nullable=False)
    q8 = db.Column(db.String, nullable=False)
    q9 = db.Column(db.String, nullable=False)
    q10 = db.Column(db.String, nullable=False)
    q11 = db.Column(db.String, nullable=False)

    # For debugging and printing user instances
    def __repr__(self):
        return f"User ID: {self.id}, Survey Responses: {[self.q1, self.q2, self.q3, self.q4, self.q5, self.q6, self.q7, self.q8, self.q9, self.q10, self.q11]}"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/survey', methods=['GET'])
def survey():
    return render_template('survey.html')

@app.route('/user', methods=['POST'])
def userResponses():
    # Retrieve form data
    responses = Response(
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
    
    # Store the user response in the database
    db.session.add(responses)
    db.session.commit()  # Commit the session to save changes
    print("Incoming Data!!!! It's WORKING!!!")
    print(responses)  # Print the response for debugging

    # Redirect to a confirmation or thank you page after submission
    return redirect(url_for('index'))

@app.route('/responses')
def display_responses():
    # Query all responses from the database, sorted by ID
    all_responses = Response.query.order_by(Response.id).all()
    
    # Pass the responses to the template
    return render_template('responses.html', all_responses=all_responses)

with app.app_context():
    db.drop_all()  # Drops all tables
    db.create_all()  # Recreates all tables according to your models

if __name__ == "__main__": 
    app.run(debug=True)
