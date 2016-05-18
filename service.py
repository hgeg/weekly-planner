#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, jsonify
from werkzeug.debug import DebuggedApplication
from flup.server.fcgi import WSGIServer
from redis import StrictRedis
from datetime import datetime, timedelta
from calendar import monthrange

#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEBase import MIMEBase
#from email import Encoders

#from credentials import SENDER_EMAIL, SENDER_PASSWORD

app = Flask(__name__)
app.debug = True
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
rdb = StrictRedis('localhost',6379,3)
HOURS  = ['8:40','9:40','10:40','11:40','13:40','14:40','15:40','16:40']

censor = lambda s: "%s%s%s"%(s[0], (len(s)-2)*'*',s[-1])

def make_week_from(date):
    start = date - timedelta(days=date.weekday())
    week = map(lambda n: datetime.strftime( start + timedelta(days=n) , '%d-%m-%Y' ), range(5))
    return week

def getweek(day):
    lkey = 'weekly.lectures.my.%s'%day
    if(rdb.llen(lkey)==0): 
        print lkey
        map( lambda _: rdb.lpush(lkey, 'none') , range(8))
    return rdb.lrange(lkey,0,8)

@app.route('/weekly/')
def home():
    week  = make_week_from(datetime.today())
    lweek = zip( *map(getweek, week) )
    courses = map(lambda s: s.split(':'), rdb.smembers('weekly.courses.my'))
    return render_template('index.html', lectures=lweek, courses=courses, hours=HOURS)

@app.route('/weekly/course/all/')
def get_courses():
    courses = map(lambda s: s.split(':'), rdb.smembers('weekly.courses.my'))
    return jsonify(courses=courses)

@app.route('/weekly/course/add/',methods=['POST'])
def add_course():
    name = request.form['name']
    lecturer = request.form['lecturer']

    rdb.sadd('weekly.courses.my','%s:%s'%(name,lecturer))
    return jsonify(message='ok',course=name)

@app.route('/weekly/lecture/add/',methods=['POST'])
def add_lecture():
    course = request.form['name']
    day = request.form['day']
    hour = request.form['hour']
    week  = make_week_from(datetime.today())
    lkey = 'weekly.lectures.my.%s'%week[int(day)]
    if(rdb.llen(lkey)==0):
        map( rdb.lpush(lkey, 'none'), range(5))
    rdb.lset(lkey, int(HOURS.index(hour)), course)
    return jsonify(message='ok',course=course)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80,debug=True)
    #WSGIServer(app).run()
