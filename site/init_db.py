#!/usr/bin/env python
# coding: utf-8

# # Database Load

# In[2]:


from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from flask import render_template
import csv
import json
import glob
import psycopg2

app = Flask(__name__)

app.config['DEBUG'] = True
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user='postgres',pw='********',url='localhost',db='country_test')
'postgresql+psycopg2://postgres:Virginis1212@localhost/country_test'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# In[ ]:





# In[2]:


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })


class Countries(BaseModel, db.Model):
    """Model for the countries table"""
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key = True)
    iso_a3 = db.Column(db.String())
    country_name = db.Column(db.String())
    indicator_code = db.Column(db.String())
    year = db.Column(db.Integer)
    value = db.Column(db.String())
    
    def __init__(self, id, iso_a3, country_name, indicator_code, year, value):
        self.id = id
        self.iso_a3 = iso_a3
        self.country_name = country_name
        self.indicator_code = indicator_code
        self.year = year
        self.value = value


# In[3]:


db.drop_all()
db.create_all()


# In[4]:


# Get all .csv files in ../Output_Data directory
csvlist = [f for f in glob.glob("../Output_data/*.csv")]
csvlist


# In[5]:


alldata = []
for csvfile in csvlist:
    with open(csvfile, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        newdata = [row for row in reader]
        alldata.append(newdata)
len(alldata)


# In[6]:


alldata[2][0][0]


# In[7]:


def get_grid_type(grid):
    if 'Year' in grid[0]:
        return 'row_by_year'
    else:
        for year_to_check in range(1960, 2999):
            if str(year_to_check) in grid[0]:
                return 'col_by_year'
    return 'undetermined'


# In[10]:


def find_key_cols_for_by_year(grid):
    started_flag = False
    country_name_ix = -1
    country_code_ix = -1
    indicator_code_ix = -1
    first_year_ix = -1
    last_year_ix = -1
    num_cols = len(grid[0])
    for col_ix in range(num_cols):
        if grid[0][col_ix] == 'Country_Name':
            country_name_ix = col_ix
        elif grid[0][col_ix] == 'Country Name':
            country_name_ix = col_ix
        elif grid[0][col_ix] == 'Country_Code':
            country_code_ix = col_ix
        elif grid[0][col_ix] == 'Country Code':
            country_code_ix = col_ix
        elif grid[0][col_ix] == 'Indicator_Code':
            indicator_code_ix = col_ix
        elif grid[0][col_ix] == 'Indicator Code':
            indicator_code_ix = col_ix
        else:
            try:
                year_col = int(grid[0][col_ix])
            except ValueError:
                pass
            else:
                if (year_col > 1960) and (year_col < 2999):
                    if started_flag:
                        last_year_ix = col_ix
                    else:
                        first_year_ix = col_ix
                        last_year_ix = col_ix
                        started_flag = True
    return country_name_ix, country_code_ix, indicator_code_ix, first_year_ix, last_year_ix


# In[11]:


def find_key_cols_for_by_row(grid):
    country_name_ix = -1
    country_code_ix = -1
    indicator_code_ix = -1
    year_ix = -1
    num_cols = len(grid[0])
    for col_ix in range(num_cols):
        if grid[0][col_ix] == 'Country_Name':
            country_name_ix = col_ix
        elif grid[0][col_ix] == 'Country Name':
            country_name_ix = col_ix
        elif grid[0][col_ix] == 'Country_Code':
            country_code_ix = col_ix
        elif grid[0][col_ix] == 'Country Code':
            country_code_ix = col_ix
        elif grid[0][col_ix] == 'Indicator_Code':
            indicator_code_ix = col_ix
        elif grid[0][col_ix] == 'Indicator Code':
            indicator_code_ix = col_ix
        elif grid[0][col_ix] == 'Year':
            year_ix = col_ix
    return country_name_ix, country_code_ix, indicator_code_ix, year_ix


# In[12]:


def process_by_year(grid, global_id):
    added_count = 0
    cname_col, ccode_col, icode_col, firstyr_col, lastyr_col = find_key_cols_for_by_year(grid)
    if (cname_col < 0) or (ccode_col < 0) or (icode_col < 0) or (firstyr_col < 0) or (lastyr_col < 0):
        print('Unable to parse csv data')
        return added_count
    at_header = True
    for row in grid:
        if at_header:
            at_header = False
            continue
        else:
            ccode = row[ccode_col]
            cname = row[cname_col]
            icode = row[icode_col]
            for year_ix in range(firstyr_col, lastyr_col + 1):
                iyear = int(grid[0][year_ix])
                ivalue = row[year_ix]
                if ivalue:
                    data_to_add = Countries(global_id, ccode, cname, icode, iyear, ivalue)
                    db.session.add(data_to_add)
                    db.session.commit
                    global_id += 1
                    added_count += 1
    return added_count


# In[13]:


def process_by_row(grid, global_id):
    added_count = 0
    cname_col, ccode_col, icode_col, yr_col = find_key_cols_for_by_row(grid)
    if (cname_col < 0) or (ccode_col < 0) or (icode_col < 0) or (yr_col < 0):
        print('Unable to parse csv data')
        return added_count
    at_header = True
    for row in grid:
        if at_header:
            at_header = False
            continue
        else:
            ccode = row[ccode_col]
            cname = row[cname_col]
            icode = row[icode_col]
            iyear = int(row[yr_col])
            ivalue = row[yr_col + 1]
            if ivalue:
                data_to_add = Countries(global_id, ccode, cname, icode, iyear, ivalue)
                db.session.add(data_to_add)
                db.session.commit
                global_id += 1
                added_count += 1
    return added_count


# In[ ]:





# In[14]:


global_id = 0
for two_d_grid in alldata:
    grid_type = get_grid_type(two_d_grid)
    if grid_type == 'col_by_year':
        num_added = process_by_year(two_d_grid, global_id)
        print('Grid with multiple years processed: added ' + str(num_added))
        global_id += num_added
    elif grid_type == 'row_by_year':
        num_added = process_by_row(two_d_grid, global_id)
        print('Grid with one year per row processed: added ' + str(num_added))
        global_id += num_added


# In[19]:


test_result = Countries.query.filter_by(indicator_code ='SH.STA.BRTC.ZS').order_by(Countries.iso_a3).all()


# In[20]:


len(test_result)




