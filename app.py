from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api


# Create the application instance
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    return "Puente's Flask API"

if __name__ == '__main__':
    app.run(debug=True)