# Import necessary libraries from Flask and SQLAlchemy
from flask import Flask, abort, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__,template_folder='templates', static_folder='StaticFile')

#SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Disable tracking modifications to save resources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database object
db = SQLAlchemy(app)

# Defined a 'Response' database table model. Stores a user ID and answers to 10 questions (answers stored as integers depending on what they pick)
class Response(db.Model):
    __tablename__ = 'responses'
    
    # Primary key for identifying each user
    id = db.Column(db.Integer, primary_key=True)
    
    # Survey response placeholders for 10 questions, each with a value between 1 and 5
    q1 = db.Column(db.Integer, nullable=False)
    q2 = db.Column(db.Integer, nullable=False)
    q3 = db.Column(db.Integer, nullable=False)
    q4 = db.Column(db.Integer, nullable=False)
    q5 = db.Column(db.Integer, nullable=False)
    q6 = db.Column(db.Integer, nullable=False)
    q7 = db.Column(db.Integer, nullable=False)
    q8 = db.Column(db.Integer, nullable=False)
    q9 = db.Column(db.Integer, nullable=False)
    q10 = db.Column(db.Integer, nullable=False)

    # For debugging and printing user instances
    def __repr__(self):
        return f"User ID: {self.id}, Survey Responses: {[self.q1, self.q2, self.q3, self.q4, self.q5, self.q6, self.q7, self.q8, self.q9, self.q10]}"

# Defined a temporary global ID variable to handle incrementing IDs
# we should consider using autoincrement in the DB in the future
global globalID 
globalID = 0

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/survey', methods=['GET'])
def survey():
    return render_template('survey.html')

@app.route('/user', methods=['POST'])
def addUserResponses():
    # TODO get form data: waiting on html/css to be finalized
    '''
    globalID = globalID + 1

    id = globalID
    q1 = request.form.get('name_property_1')
    q2 = request.form.get('name_property_2')
    q3 = request.form.get('name_property_3')
    q4 = request.form.get('name_property_4')
    q5 = request.form.get('name_property_5')
    q6 = request.form.get('name_property_6')
    q7 = request.form.get('name_property_7')
    q8 = request.form.get('name_property_8')
    q9 = request.form.get('name_property_9')
    q10 = request.form.get('name_property_10')
    q11 = request.form.get('name_property_11')
    
    user = User(id=id, q1=q1,q2=q2,q3=q3,q4=q4,q5=q5,q6=q6,q7=q7,q8=q8,q9=q9,q10=q10,q11=q11)

    db.session.add(user)
    db.session.commit()

    return render_template('response.html', surveyResponse=user)
    '''
    return "POST Redirect"

@app.route('/user/<int:id>', methods=['GET'])
def userResponses(id):
    #surveyResponse = db.session.get(surveyResponse, id)
    #return render_template('response.html', surveyResponse=surveyResponse)
    return "GET Responses for user id: " + str(id)

if __name__ == "__main__":
    # Create database tables if they do not exist yet
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
