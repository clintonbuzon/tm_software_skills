# EC2 prerequsites
# -----------------------------------------------
# Python 3.7.3
# -----------------------------------------------
# sudo yum update
# sudo yum install python3
# sudo yum install sqlite
# curl -O https://bootstrap.pypa.io/get-pip.py
# python3 get-pip.py --user
# rm get-pip.py
# pip install python-dateutil --user
# pip install Django==2.1.* --user
# -----------------------------------------------
import csv
from dateutil import parser
import sqlite3
import os
import shutil

# Parameters to be edited
source_filename = "dailycheckins.csv"
temp_database = "temp.db"
final_database = "dailycheckins.db"
django_dir = "mysite/"

sql_create_dailycheckins_table = "CREATE TABLE IF NOT EXISTS dailycheckins (id INTEGER PRIMARY KEY, user text, original_timestamp text, hours text, project text, cleaned_timestamp);"

# Function which creates databased connection.
# If the provided file does not exist, this function will automaticall create new db file
# Input: database file name
# Return: conn
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e) 
    return conn

# Function which executed a query creating a table
# Input: conn and create table statement
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# Function which executes an insert statement provided data to insert
# Input: conn and data to be inserted in tuple format
def insert_db(conn, data):
    try:
        sql = "INSERT INTO dailycheckins(user, original_timestamp, hours, project, cleaned_timestamp) VALUES (?,?,?,?,?)"
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
    except Error as e:
        print(e)

# Function which checks if a string contains russian dates/month
# Input: string, in this case the dirty timestamp
# Return: russian date/month found
def check_if_russian_date(timestamp):
    russian_months = ['декабря','сентября', 'ноября', 'октября', 'августа', 'июля', 'июня', 'мая', 'апреля', 'марта', 'февраля', 'января']
    for i in russian_months:
        if i in timestamp:
            return i

# Function which returns english month in string when provided russian month
# Input: russian month in string
# Return: english month in string
def get_eng_month(month):   
    russian_months = [
            {'r_month' : 'января', 'e_month' : 'January'},
            {'r_month' : 'февраля', 'e_month' : 'February'},
            {'r_month' : 'марта', 'e_month' : 'March'},
            {'r_month' : 'апреля', 'e_month' : 'April'},
            {'r_month' : 'мая', 'e_month' : 'May'},
            {'r_month' : 'июня', 'e_month' : 'June'},
            {'r_month' : 'июля', 'e_month' : 'July'},
            {'r_month' : 'августа', 'e_month' : 'August'},
            {'r_month' : 'сентября', 'e_month' : 'September'},
            {'r_month' : 'октября', 'e_month' : 'October'},
            {'r_month' : 'ноября', 'e_month' : 'November'},
            {'r_month' : 'декабря', 'e_month' : 'December'}]

    result = [x for x in russian_months if x['r_month'] == month]
    return result[0].get('e_month')

# Function which cleans the timestamp
# Assumption, all timestamps on the file are in UTC
# Cleaning steps:
# 1. Check if timestamp has provided timezone, if not append UTC tag at the end
# 2. Check if timestamp contains russian date/month. If yes, we replace it with english version
# 3. Convert the string to datetime object using dateutil.parser.
# 4. Return uniform formatted timestamp as string
def clean_timestamp(timestamp):
    final_timestamp = timestamp
    
    # Check if timestamp has provided timezone, if not append UTC tag at the end
    if timestamp[-3:] != "UTC":
        final_timestamp = timestamp + " UTC"
    russian_date = check_if_russian_date(timestamp)
    
    # Check if timestamp contains russian date/month. If yes, we replace it with english version
    if russian_date:
        final_timestamp = final_timestamp.replace(russian_date,get_eng_month(russian_date))
    
    # Convert the string to datetime object using dateutil.parser.
    dt = parser.parse(final_timestamp) # datetime object
    
    # Return uniform formatted timestamp as string
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f%z")


# main, code starts here
if __name__ == '__main__':
    # create a database connection
    conn = create_connection(temp_database)

    # create dailycheckins tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_dailycheckins_table)
    else:
        print("Error! cannot create the database connection.")

    # scan through dailycheckins.csv file
    with open(source_filename,encoding="utf8") as csv_file: # since file contains russian dates, we use encoding utf-8
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0: # print headers, ignore do not insert
                print("Column names are {}".format(row))
                line_count += 1
            else: # actual rows to process
                row.append(clean_timestamp(row[1])) # append cleaned timestamp, retain raw timestamp for future reference
                if row[0] == "": # checks if user is blank
                    row[0] = "<blank>" # if yes, replaces with "<blank>" string
                print("Inserting: {}".format(tuple(row)))
                insert_db(conn, tuple(row)) # insert row to database
                line_count += 1
        print(f'Processed {line_count} lines.') # print number of rows processed

    conn.close() # close connection. Not closing it causes issues when copying and moving files

    # create copy of database for submission
    shutil.copyfile(temp_database, final_database)

    # move a copy of the database to mysite database
    os.replace(temp_database, django_dir+"db.sqlite3")