#! python3

# Imports
from flask import Flask, render_template
from flask_restful import Resource, Api

# Set Up Application

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

# Default Route for Landing Page
@app.route("/")
def index():
    return render_template('main.html')

# API Routes


class BALevel(Resource):
    def get(self, level):
        return None


if __name__ == '__main__':
    app.run(debug=True)
