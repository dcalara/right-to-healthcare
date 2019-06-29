from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
import os
import pandas as pd
import numpy as np
from models import db, Countries

app = Flask(__name__)

DB_URL = os.environ['DATABASE_URL']
app.config['DEBUG'] = False
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

    # Generate a list of unique iso_a3 values from the DataFrame column
    isoa3s = list(set(dfm['isoa3'].values))
    # Generate a dictionary of correlation coefficients when 4 or more data 
    # points are available, using iso_a3 codes as keys
    for isoa3 in isoa3s:
        dfm1c = dfm.loc[dfm['isoa3'] == isoa3]
        newcorr = "null"
        if len(dfm1c) > 3:
            newcorr = dfm1c['value1'].astype('float').corr(dfm1c['value2'].astype('float'))
            if np.isnan(newcorr):
                newcorr = "null"
        corrs[isoa3] = newcorr
    return jsonify(corrs)

@app.route("/ts_a3/<isoa3>/<var1>/<var2>")
def double_time_series_single_country(isoa3,var1,var2):
    """Return JSON with year1, value1, year2, value2 arrays for a given country.
    Intended mainly for convenient use in plotting routines."""

    code1 = var1.replace("-",".")
    code2 = var2.replace("-",".")

    query1 = db.session.query(Countries).\
        filter_by(indicator_code=code1).\
        filter_by(iso_a3=isoa3).\
        statement
    df1 = pd.read_sql_query(query1, db.session.bind)
    df1.columns = ['pk1','isoa3','name1','code1','year','value1']
    df1 = df1.sort_values('year')
    query2 = db.session.query(Countries).\
        filter_by(indicator_code=code2).\
        filter_by(iso_a3=isoa3).\
        statement
    df2 = pd.read_sql_query(query2, db.session.bind)  
    df2.columns = ['pk2','isoa3','name2','code2','year','value2']
    df2 = df2.sort_values('year')

    plot_data = dict()
    plot_data['year1'] = df1['year'].tolist()
    plot_data['value1'] = df1['value1'].tolist()
    plot_data['year2'] = df2['year'].tolist()
    plot_data['value2'] = df2['value2'].tolist()
        
    return jsonify(plot_data)

@app.route("/ts_a3/<isoa3>/<var1>")
def single_time_series_single_country(isoa3,var1):
    """Return JSON with year, value arrays for a given country.
    Intended mainly for convenient use in plotting routines."""

    code1 = var1.replace("-",".")

    query1 = db.session.query(Countries).\
        filter_by(indicator_code=code1).\
        filter_by(iso_a3=isoa3).\
        statement
    df1 = pd.read_sql_query(query1, db.session.bind)
    df1.columns = ['pk1','isoa3','name1','code1','year','value1']
    df1 = df1.sort_values('year')

    plot_data = dict()
    plot_data['year1'] = df1['year'].tolist()
    plot_data['value1'] = df1['value1'].tolist()
        
    return jsonify(plot_data)

@app.route("/ts_all/<var1>")
def time_series_all_years(var1):
    """Return JSON array of nested objects, each object has a 'year' and 'data'
    attribute, where 'data' lists iso_a3 codes and values. Returns all years."""

    code1 = var1.replace("-",".")
    list_by_year = []

    query1 = db.session.query(Countries).\
        filter_by(indicator_code=code1).\
        statement
    df1 = pd.read_sql_query(query1, db.session.bind)
    df1.columns = ['pk1','isoa3','name1','code1','year','value1']
    df1 = df1.sort_values('year')
    first_year = df1['year'].astype('int').min()
    last_year = df1['year'].astype('int').max()
    for year in range(first_year,last_year+1):
        df_year = df1.loc[df1['year'].astype('int') == year]
        outer_dict = dict()
        outer_dict['year'] = year
        if(not df_year.empty):
            isoa3_dict = {isoa3:value for isoa3,value in zip(df_year['isoa3'].tolist(),df_year['value1'].tolist())}
        else:
            isoa3_dict = dict()
        outer_dict['data'] = isoa3_dict
        list_by_year.append(outer_dict)
        
    return jsonify(list_by_year)

@app.route("/ts_all/<var1>/<year1>/<year2>")
def time_series_rangeof_years(var1, year1, year2):
    """Return JSON array of nested objects, each object has a 'year' and 'data'
    attribute, where 'data' lists iso_a3 codes and values. Returns all years in
    range year1 to year2 inclusive."""

    code1 = var1.replace("-",".")
    try:
        year1 = int(year1)
    except ValueError:
        year1 = 1960
    
    try:
        year2 = int(year2)
    except ValueError:
        year2 = 2019

    list_by_year = []

    query1 = db.session.query(Countries).\
        filter_by(indicator_code=code1).\
        filter(Countries.year >= year1).\
        filter(Countries.year <= year2).\
        statement
    df1 = pd.read_sql_query(query1, db.session.bind)
    df1.columns = ['pk1','isoa3','name1','code1','year','value1']
    df1 = df1.sort_values('year')
    first_year = year1
    last_year = year2
    for year in range(first_year,last_year+1):
        df_year = df1.loc[df1['year'].astype('int') == year]
        outer_dict = dict()
        outer_dict['year'] = year
        if(not df_year.empty):
            isoa3_dict = {isoa3:value for isoa3,value in zip(df_year['isoa3'].tolist(),df_year['value1'].tolist())}
        else:
            isoa3_dict = dict()
        outer_dict['data'] = isoa3_dict
        list_by_year.append(outer_dict)
        
    return jsonify(list_by_year)

@app.route("/ts_all/<var1>/<year>")
def time_series_single_year(var1, year):
    """Return JSON object listing values with iso_a3 codes as keys for each
    country for the specified year"""

    code1 = var1.replace("-",".")
    try:
        year = int(year)
    except ValueError:
        return jsonify(dict())
    
    query1 = db.session.query(Countries).\
        filter_by(indicator_code=code1).\
        filter_by(year=year).\
        statement
    df1 = pd.read_sql_query(query1, db.session.bind)
    if (not df1.empty):
        df1.columns = ['pk1','isoa3','name1','code1','year','value1']
        isoa3_dict = {isoa3:value for isoa3,value in zip(df1['isoa3'].tolist(),df1['value1'].tolist())}
    else:
        isoa3_dict = dict()
        
    return jsonify(isoa3_dict)


if __name__ == '__main__':
    app.run()