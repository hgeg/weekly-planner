#!/usr/bin/env python
from flask import Flask, request, render_template
from werkzeug.debug import DebuggedApplication
from flup.server.fcgi import WSGIServer

#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEBase import MIMEBase
#from email import Encoders

#from credentials import SENDER_EMAIL, SENDER_PASSWORD

app = Flask(__name__)
app.debug = True
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

censor = lambda s: "%s%s%s"%(s[0], (len(s)-2)*'*',s[-1])

@app.route('/weekly/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="localhost",port=80,debug=True)
    #WSGIServer(app).run()
