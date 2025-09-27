from flask import Flask, render_template, request
from pymysql import connections
import os
import random
import argparse

app = Flask(__name__)

DBHOST = os.environ.get("MYSQL_HOST", "localhost")
DBUSER = os.environ.get("MYSQL_USER", "root")
DBPASSWORD = os.environ.get("MYSQL_PASSWORD", "password")
DATABASE = os.environ.get("MYSQL_DB", "employees")
APP_BG_COLOR = os.environ.get('BG_COLOR') or "lime"
DBPORT = int(os.environ.get("DBPORT", "3306"))

db_conn = connections.Connection(
    host=DBHOST, port=DBPORT, user=DBUSER, password=DBPASSWORD, database=DATABASE
)

output = {}
table = 'employee'

color_codes = {
    "red": "#e74c3c", "green": "#16a085", "blue": "#89CFF0", "blue2": "#30336b",
    "pink": "#f4c2c2", "darkblue": "#130f40", "lime": "#C1FF9C",
}

SUPPORTED_COLORS = ",".join(color_codes.keys())
COLOR = random.choice(list(color_codes.keys()))

@app.route("/", methods=['GET', 'POST'])
@app.route("/blue", methods=['GET', 'POST'])
@app.route("/pink", methods=['GET', 'POST'])
@app.route("/lime", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', color=color_codes[COLOR])

@app.route("/about", methods=['GET','POST'])
@app.route("/blue/about", methods=['GET','POST'])
@app.route("/pink/about", methods=['GET','POST'])
@app.route("/lime/about", methods=['GET','POST'])
def about():
    return render_template('about.html', color=color_codes[COLOR])

@app.route("/addemp", methods=['POST'])
@app.route("/blue/addemp", methods=['POST'])
@app.route("/pink/addemp", methods=['POST'])
@app.route("/lime/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']
    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()
    try:
        cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = f"{first_name} {last_name}"
    finally:
        cursor.close()
    return render_template('addempoutput.html', name=emp_name, color=color_codes[COLOR])

@app.route("/getemp", methods=['GET', 'POST'])
@app.route("/blue/getemp", methods=['GET', 'POST'])
@app.route("/pink/getemp", methods=['GET', 'POST'])
@app.route("/lime/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", color=color_codes[COLOR])

@app.route("/fetchdata", methods=['GET','POST'])
@app.route("/blue/fetchdata", methods=['GET','POST'])
@app.route("/pink/fetchdata", methods=['GET','POST'])
@app.route("/lime/fetchdata", methods=['GET','POST'])
def FetchData():
    emp_id = request.form['emp_id']
    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location from employee where emp_id=%s"
    cursor = db_conn.cursor()
    try:
        cursor.execute(select_sql, (emp_id))
        result = cursor.fetchone()
        if result:
            output["emp_id"] = result[0]
            output["first_name"] = result[1]
            output["last_name"] = result[2]
            output["primary_skills"] = result[3]
            output["location"] = result[4]
            return render_template("getempoutput.html", id=output["emp_id"], fname=output["first_name"],
                                   lname=output["last_name"], interest=output["primary_skills"], location=output["location"], color=color_codes[COLOR])
    except Exception as e:
        print(e)
    finally:
        cursor.close()
    return render_template("getemp.html", error_message="Employee not found or database error", color=color_codes[COLOR])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', required=False)
    args = parser.parse_args()
    if args.color:
        COLOR = args.color
    elif APP_BG_COLOR:
        COLOR = APP_BG_COLOR
    if COLOR not in color_codes:
        exit(1)
    app.run(host='0.0.0.0', port=8080, debug=True)