# Import necessary libraries from SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Initialize the database object
db = SQLAlchemy()

# Define the association table for Period and Question
PeriodQuestion = db.Table(
    'periodquestion',
    db.Column('period_id', db.Integer, db.ForeignKey('periods.id')),
    db.Column('question_id', db.Integer, db.ForeignKey('questions.id')),
    db.PrimaryKeyConstraint('period_id', 'question_id')
)

# Define the Period model
class Period(db.Model):
    __tablename__ = 'periods'
    
    # Primary key for identifying each period ex. Spring 2024
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    periodName = db.Column(db.String(30), nullable=False)
    numDoubles = db.Column(db.Integer, nullable=False)
    numQuads = db.Column(db.Integer, nullable=False)

    periodquestions = db.relationship('Question', secondary=PeriodQuestion, backref='questionperiods')

# Define the Response model
class Response(db.Model):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    q1 = db.Column(db.String(255), nullable=False, default="freshman")
    q2 = db.Column(db.String(255), nullable=False, default="Computer science")
    q3 = db.Column(db.String(255), nullable=False, default="yes")
    q4 = db.Column(db.String(255), nullable=False, default="3")
    q5 = db.Column(db.String(255), nullable=False, default="10pm")
    q6 = db.Column(db.String(255), nullable=False, default="10pm-midnight")
    q7 = db.Column(db.String(255), nullable=False, default="Quiet Study")
    q8 = db.Column(db.String(255), nullable=False, default="Art")
    q9 = db.Column(db.String(255), nullable=False, default="moderate")
    q10 = db.Column(db.String(255), nullable=False, default="tidy")
    q11 = db.Column(db.String(255), nullable=False, default="avoid")

# Define the Question model
class Question(db.Model):
    __tablename__ = 'questions'
    
    # Primary key for identifying each question
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(255), nullable=False)
    subtext = db.Column(db.String(255))
    options = db.Column(db.String(255), nullable=False)
    questiontype = db.Column(db.Integer, nullable=False)

# Define the Student model
class Student(db.Model):
    __tablename__ = 'students'
    
    # Primary key for identifying each student
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    placed = db.Column(db.Boolean, default=False)

    response = db.relationship('Response', uselist=False, backref='student')
