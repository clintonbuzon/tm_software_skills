# sudo yum update
# sudo yum install python3
# sudo yum install sqlite
# curl -O https://bootstrap.pypa.io/get-pip.py
# python3 get-pip.py --user
# pip install python-dateutil --user
# pip install Django==2.1.* --user
# python manage.py runserver 0.0.0.0:8000

import csv
from dateutil import parser
import sqlite3
import os

database = "db_file.db"
cleaned_csv = 'dailycheckins_cleaned.csv'
django_dir = "mysite/"

sql_create_dailycheckins_table = """ CREATE TABLE IF NOT EXISTS dailycheckins (
                                        id INTEGER PRIMARY KEY,
                                        user text,
                                        original_timestamp text,
                                        hours text,
                                        project text,
                                        cleaned_timestamp
                                    ); """

temp = "drop table dailycheckins;"

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(database)
        return conn
    except Error as e:
        print(e)
 
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_db(conn, data):
    sql = "INSERT INTO dailycheckins(user, original_timestamp, hours, project, cleaned_timestamp) VALUES (?,?,?,?,?)"
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()

def check_if_russian_date(timestamp):
    russian_months = ['декабря','сентября', 'ноября', 'октября', 'августа', 'июля', 'июня', 'мая', 'апреля', 'марта', 'февраля', 'января']
    for i in russian_months:
        if i in timestamp:
            return i

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
            {'r_month' : 'декабря', 'e_month' : 'December'}
    ]

    result = [x for x in russian_months if x['r_month'] == month]
    return result[0].get('e_month')

def clean_timestamp(timestamp):
    final_timestamp = timestamp
    if timestamp[-3:] != "UTC":
        final_timestamp = timestamp + " UTC"
    russian_date = check_if_russian_date(timestamp)
    if russian_date:
        final_timestamp = final_timestamp.replace(russian_date,get_eng_month(russian_date))
        #print(final_timestamp)
    dt = parser.parse(final_timestamp)
    #return dt
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f%z")

# create a database connection
conn = create_connection(database)

# create tables
if conn is not None:
    # create projects table
    create_table(conn, sql_create_dailycheckins_table)
else:
    print("Error! cannot create the database connection.")

with open('dailycheckins.csv',encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print("Column names are {}".format(row))
            line_count += 1
        else:
            row.append(clean_timestamp(row[1]))
            print("Inserting: {}".format(tuple(row)))
            insert_db(conn, tuple(row))
            line_count += 1
            #timestamps.append(row[1])
    print(f'Processed {line_count} lines.')

conn.close()

os.replace(database, django_dir+"db.sqlite3")