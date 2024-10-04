from flask import Flask, abort, render_template

app = Flask(__name__,template_folder='templates', static_folder='StaticFile')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/survey', methods=['GET'])
def survey():
    return render_template('survey.html')

@app.route('/user/<int:id>', methods=['GET', 'POST'])
def userResponses(id):
    return "Responses for user id: " + str(id)

if __name__ == "__main__":
    app.run(debug=True)

