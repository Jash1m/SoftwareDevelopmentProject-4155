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
    
    responses = db.relationship('Response', backref='period')
    periodquestions = db.relationship('Question', secondary=PeriodQuestion, backref='questionperiods')

# Define the Response model
class Response(db.Model):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    period_id = db.Column(db.Integer, db.ForeignKey('periods.id'))
    q1 = db.Column(db.String(255))
    q2 = db.Column(db.String(255))
    q3 = db.Column(db.String(255))
    q4 = db.Column(db.String(255))
    q5 = db.Column(db.String(255))
    q6 = db.Column(db.String(255))
    q7 = db.Column(db.String(255))
    q8 = db.Column(db.String(255))
    q9 = db.Column(db.String(255))
    q10 = db.Column(db.String(255))
    q11 = db.Column(db.String(255))
    q12 = db.Column(db.String(255))
    q13 = db.Column(db.String(255))
    q14 = db.Column(db.String(255))
    q15 = db.Column(db.String(255))

# Define the Question model
class Question(db.Model):
    __tablename__ = 'questions'
    
    # Primary key for identifying each question
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(255), nullable=False)
    subtext = db.Column(db.String(255))
    options = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255), nullable=False)
    questiontype = db.Column(db.Integer, nullable=False)

# Define the Student model
class Student(db.Model):
    __tablename__ = 'students'
    
    # Primary key for identifying each student
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    placed = db.Column(db.Boolean, default=False)
    group_id = db.Column(db.Integer, db.ForeignKey('roommategroups.id'))

    response = db.relationship('Response', uselist=False, backref='student')

class RoommateGroup(db.Model):
    __tablename__ = 'roommategroups'

    id = db.Column(db.Integer, primary_key=True)

    students = db.relationship('Student', backref='group')


class PQLog(db.Model):
    __tablename__ = 'pqlog'

    pq_id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255))
    actiontime = db.Column(db.DateTime)
    period_id = db.Column(db.Integer)
    question_id = db.Column(db.Integer) 

periodquestion_log = db.DDL('''\
CREATE TRIGGER periodquestion_i AFTER INSERT ON periodquestion
    FOR EACH ROW
    INSERT INTO pqlog (action, actiontime, period_id, question_id)
    VALUES('insert', NOW(), NEW.period_id, NEW.question_id);
                            
CREATE TRIGGER periodquestion_u AFTER UPDATE ON periodquestion
    FOR EACH ROW
    INSERT INTO pqlog (action, actiontime, period_id, question_id)
    VALUES('update', NOW(), NEW.period_id, NEW.question_id);
                            
CREATE TRIGGER periodquestion_d AFTER DELETE ON periodquestion
    FOR EACH ROW
    INSERT INTO pqlog (action, actiontime, period_id, question_id)
    VALUES('delete', NOW(), OLD.period_id, OLD.question_id);
    ''')
db.event.listen(PeriodQuestion, 'after_create', periodquestion_log)

class PLog(db.Model):
    __tablename__ = 'plog'

    pq_id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255))
    actiontime = db.Column(db.DateTime)
    id = db.Column(db.Integer)
    periodName = db.Column(db.String(30), nullable=False)
    numDoubles = db.Column(db.Integer, nullable=False)
    numQuads = db.Column(db.Integer, nullable=False)

period_log = db.DDL('''\
CREATE TRIGGER period_i AFTER INSERT ON periods
    FOR EACH ROW
    INSERT INTO plog (action, actiontime, id, periodName, numDoubles, numQuads)
    VALUES('insert', NOW(), NEW.id, NEW.periodName, NEW.numDoubles, NEW.numQuads);
                            
CREATE TRIGGER period_u AFTER UPDATE ON periods
    FOR EACH ROW
    INSERT INTO plog (action, actiontime, id, periodName, numDoubles, numQuads)
    VALUES('update', NOW(), NEW.id, NEW.periodName, NEW.numDoubles, NEW.numQuads);
                            
CREATE TRIGGER period_d AFTER DELETE ON periods
    FOR EACH ROW
    INSERT INTO plog (action, actiontime, id, periodName, numDoubles, numQuads)
    VALUES('delete', NOW(), OLD.id, OLD.periodName, OLD.numDoubles, OLD.numQuads);
    ''')
db.event.listen(Period.__table__, 'after_create', period_log)
