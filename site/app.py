from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'my_database',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/country_test'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)

#from models import Countries 

@app.route('/')
def landing():
    """Produces landing page"""
    return render_template("index.html")

@app.route("/about.html")
def about():
    """About the project"""
    return render_template("about.html")

@app.route("/dataviz.html")
def dataviz():
    """Data visualization"""
    return render_template("dataviz.html")

@app.route("/globe.html")
def globe():
    """Interactive globe"""
    return render_template("globe.html")

@app.route("/index.html")
def go_to_index():
    """Return to index page"""
    return render_template("index.html")

@app.route("/testroute1")
def testroute():
    """Return test data"""
    test_data = {'CAN':0.1,
                 'USA':0.2,
                 'MEX':0.3,
                 'FRA':0.4,
                 'ARG':0.5,
                 'AUS':0.6,
                 'BLR':0.7,
                 'JPN':0.8,
                 'KAZ':0.9,
                 'MOZ':0.98}
    return jsonify(test_data)

if __name__ == '__main__':
    app.run()