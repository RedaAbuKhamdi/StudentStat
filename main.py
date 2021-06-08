from flask import Flask, escape, request
from database.database_connection import *
from flask import render_template
import pandas as pd

app = Flask(__name__)
# dev test only
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/', methods = ["GET"])
def index():

    return render_template('index.html')

@app.route('/info', methods = ["GET"])
def info():
    teachers = select(teacher_names)
    groups = select(group_names)
    return render_template('info.html', teachers = teachers,groups =  groups)

@app.route('/get_lessons', methods = ['GET'])
def get_lessons():
    teacher_name = request.args.get('teacher_name')
    group_name = request.args.get('group_name')
    data = select(lesson_data.format(teacher_name, group_name))
    data = pd.DataFrame.from_dict(data)
    return data.to_html()

app.run()

