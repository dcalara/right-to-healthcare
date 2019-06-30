from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import csv
import glob
import psycopg2
import os

# db configuration
app = Flask(__name__)

app.config['DEBUG'] = False
DB_URL = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Countries(db.Model):
    """Model for the countries table"""
    __tablename__ = 'countries3'

    id = db.Column(db.Integer, primary_key = True)
    iso_a3 = db.Column(db.String())
    country_name = db.Column(db.String())
    indicator_code = db.Column(db.String())
    year = db.Column(db.Integer)
    value = db.Column(db.String())

def import_csv_data():
    """Grab a list of csv's in the folder Output_data, then transform each
    into a 'list of lists' inside of a third list."""
    csvlist = [f for f in glob.glob("../Output_data/*.csv")]
    #alldata will be a '3-D' list, list of csvs -> list of rows -> list of columns
    data = []
    for csvfile in csvlist:
        with open(csvfile, encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            newdata = [row for row in reader]
            data.append(newdata)
    return data

def get_grid_type(grid):
    """Parse a list of lists derived from a csv file, use contents
    of header row to determine whether multi-year data is listed with
    one column per year, or if each year uses a separate row"""
    if 'Year' in grid[0]:
        return 'year_by_row'
    else:
        for year_to_check in range(1960, 2999):
            if str(year_to_check) in grid[0]:
                return 'year_by_col'
            elif (str(year_to_check) + '.0') in grid[0]:
                return 'year_by_col'
    #Default if neither check was successful
    return 'undetermined'

def find_key_cols_year_by_col(grid):
    """Finds the indices of the key columns in a csv file previously 
    converted to a list of lists (grid). Use when each year is a separate
    column"""
    started_flag = False
    country_name_ix = -1
    country_code_ix = -1
    indicator_code_ix = -1
    first_year_ix = -1
    last_year_ix = -1
    num_cols = len(grid[0])
    for col_ix in range(num_cols):
        if grid[0][col_ix] == 'Country':
            country_name_ix = col_ix
        elif grid[0][col_ix] == 'Entity':
            country_name_ix = col_ix
        elif grid[0][col_ix] == 'Country_Name':
            country_name_ix = col_ix
        elif grid[0][col_ix] == 'Country Name':
            country_name_ix = col_ix
        elif grid[0][col_ix] == 'Country_Code':
            country_code_ix = col_ix
        elif grid[0][col_ix] == 'Country Code':
            country_code_ix = col_ix
        elif grid[0][col_ix] == 'Country ISO3':
            country_code_ix = col_ix
        elif grid[0][col_ix] == 'Code':
            country_code_ix = col_ix
        elif grid[0][col_ix] == 'Indicator_Code':
            indicator_code_ix = col_ix
        elif grid[0][col_ix] == 'Indicator Code':
            indicator_code_ix = col_ix
        elif grid[0][col_ix] == 'Indicator Id':
            indicator_code_ix = col_ix
        else:
            #Look for column headings that are numbers
            try:
                year_col = int(float(grid[0][col_ix]))
            except ValueError:
                pass
            else:
                if (year_col > 1940) and (year_col < 2999):
                    if started_flag:
                        last_year_ix = col_ix
                    else:
                        first_year_ix = col_ix
                        last_year_ix = col_ix
                        started_flag = True
    return country_name_ix, country_code_ix, indicator_code_ix, first_year_ix, last_year_ix

def find_key_cols_year_by_row(grid):
    """Finds the indices of the key columns in a csv file previously 
    converted to a list of lists (grid). Use when each year is a separate
    row"""
    country_name_ix = -1
    country_code_ix = -1
    indicator_code_ix = -1
    year_ix = -1
    num_cols = len(grid[0])
    for col_ix in range(num_cols):
        if grid[0][col_ix] == 'Country':
            country_name_ix = col_ix
        elif grid[0][col_ix] == 'Entity':
            country_name_ix = col_ix
        elif grid[0][col_ix] == 'Country_Name':
            country_name_ix = col_ix
        elif grid[0][col_ix] == 'Country Name':
            country_name_ix = col_ix
        elif grid[0][col_ix] == 'Country_Code':
            country_code_ix = col_ix
        elif grid[0][col_ix] == 'Country Code':
            country_code_ix = col_ix
        elif grid[0][col_ix] == 'Country ISO3':
            country_code_ix = col_ix
        elif grid[0][col_ix] == 'Code':
            country_code_ix = col_ix
        elif grid[0][col_ix] == 'Indicator_Code':
            indicator_code_ix = col_ix
        elif grid[0][col_ix] == 'Indicator Code':
            indicator_code_ix = col_ix
        elif grid[0][col_ix] == 'Indicator Id':
            indicator_code_ix = col_ix
        elif grid[0][col_ix] == 'Year':
            year_ix = col_ix
    return country_name_ix, country_code_ix, indicator_code_ix, year_ix


def process_year_by_col(grid, global_id):
    """Takes data from a csv file converted to a list of lists (row/col grid)
    and adds each data point to a db.  Use when multiple years are in 
    the same row"""
    added_count = 0
    cname_col, ccode_col, icode_col, firstyr_col, lastyr_col = find_key_cols_year_by_col(grid)
    if (cname_col < 0) or (ccode_col < 0) or (icode_col < 0) or (firstyr_col < 0) or (lastyr_col < 0):
        #Abort processing if any key column indices are undetermined
        return added_count
    at_header = True
    for row in grid:
        if at_header:
            at_header = False
            continue  #Skip to next row
        else:
            ccode = row[ccode_col].strip()
            cname = row[cname_col].strip()
            icode = row[icode_col].strip()
            for year_ix in range(firstyr_col, lastyr_col + 1):
                try:
                    iyear = int(float(grid[0][year_ix]))
                    ivalue = float(row[year_ix])
                    if ivalue > 0:
                        data_to_add = Countries(iso_a3=ccode, 
                                                country_name=cname, 
                                                indicator_code=icode, 
                                                year=iyear, 
                                                value=ivalue)
                        db.session.add(data_to_add)
                        db.session.commit()
                        global_id += 1
                        added_count += 1
                except ValueError:
                    pass
    return added_count

def process_year_by_row(grid, global_id):
    """Takes data from a csv file converted to a list of lists (row/col grid)
    and adds each data point to a db.  Use when a single year's data is found in 
    one row"""
    added_count = 0
    cname_col, ccode_col, icode_col, yr_col = find_key_cols_year_by_row(grid)
    if (cname_col < 0) or (ccode_col < 0) or (icode_col < 0) or (yr_col < 0):
        #Abort adding data if any key column indices are undetermined
        return added_count
    at_header = True
    for row in grid:
        if at_header:
            at_header = False
            continue  #Skip to next row
        else:
            ccode = row[ccode_col].strip()
            cname = row[cname_col].strip()
            icode = row[icode_col].strip()
            try:
                iyear = int(float(row[yr_col]))
                ivalue = float(row[yr_col + 1])
                if ivalue > 0:
                    data_to_add = Countries(iso_a3=ccode, 
                                            country_name=cname, 
                                            indicator_code=icode, 
                                            year=iyear, 
                                            value=ivalue)
                    db.session.add(data_to_add)
                    db.session.commit()
                    global_id += 1
                    added_count += 1
            except ValueError:
                pass
    return added_count

def main():
    """Sets up Postgres database, imports a set of csv's from the Output_data file,
    then loads the data into the database based on how the data is arrayed in each csv"""
    db.drop_all()
    db.create_all()
    alldata = import_csv_data()
    #Start db primary key index (as global_id here) at 1, and track as each grid is processed
    global_id = 1
    #alldata is a list of two_d_grids (each grid is a list of lists holding the contents of one csv file)
    for two_d_grid in alldata:
        grid_type = get_grid_type(two_d_grid)
        if grid_type == 'year_by_col':
            # The processing routines add data to db as a side effect, returning # of rows added
            num_added = process_year_by_col(two_d_grid, global_id)
            global_id += num_added
            print('Added ' + str(num_added))
        elif grid_type == 'year_by_row':
            num_added = process_year_by_row(two_d_grid, global_id)
            global_id += num_added
            print('Added ' + str(num_added))
        #Do nothing if the grid type doesn't match a pre-defined template
    #Finished processing all grids
    print('Total additions:  ' + str(global_id))

if __name__ == '__main__':
    main()