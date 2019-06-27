from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
import os
import pandas as pd
import numpy as np
from models import db, Countries

app = Flask(__name__)

DB_URL = os.environ['DATABASE_URL']
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

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

@app.route("/corr/<var1>/<var2>")
def correlate_all(var1,var2):
    """Return JSON of countries with correlation coefficients for var1, var2.
    Use the indicator names with a '.' replaced with a '-'."""
    code1 = var1.replace("-",".")
    code2 = var2.replace("-",".")
    corrs = dict()

    query1 = db.session.query(Countries).\
        filter_by(indicator_code=code1).\
        statement
    df1 = pd.read_sql_query(query1, db.session.bind)
    df1.columns = ['pk1','isoa3','name1','code1','year','value1']
    query2 = db.session.query(Countries).\
        filter_by(indicator_code=code2).\
        statement
    df2 = pd.read_sql_query(query2, db.session.bind)  
    df2.columns = ['pk2','isoa3','name2','code2','year','value2']
    dfm = df1.merge(df2,how='inner',on=['isoa3','year'])

    isoa3s = list(set(dfm['isoa3'].values))

    for isoa3 in isoa3s:
        dfm1c = dfm.loc[dfm['isoa3'] == isoa3]
        newcorr = "null"
        if len(dfm1c) > 3:
            newcorr = dfm1c['value1'].astype('float').corr(dfm1c['value2'].astype('float'))
            if np.isnan(newcorr):
                newcorr = "null"
        corrs[isoa3] = newcorr
        
    
    return jsonify(corrs)

if __name__ == '__main__':
    app.run()