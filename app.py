from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "homepage \n <a href='survey'>survey</a>"

@app.route('/survey', methods=['GET'])
def survey():
    return "survey \n <a href='user/1'>survey</a>"

@app.route('/user/<int:id>', methods=['GET', 'POST'])
def userResponses(id):
    return "Responses for user id: " + str(id)

if __name__ == "__main__":
    app.run(debug=True)

