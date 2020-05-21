import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)

def decode_resp(s):
    pairs_with_equalto = s.split('&')
    resp = {}
    for item in pairs_with_equalto:
        key, value = item.split('=')
        resp[key] = value 
    return resp
def day_in_month(month,year):
    month = int(month)
    year = int(year)
    if ((year%100!=0 and year%4==0) or (year%400==0)) and month == 2:
        return 29
    elif month==2:
        return 28
    elif month in [1,3,5,7,8,10,12]:
        return 31
    else:
        return 30

def blank_divs(year,month):
    return ['' for i in range(int(datetime(int(year),int(month),1).strftime("%w")))]

def month_name(month):
    return datetime(2020,int(month),1).strftime("%B")

class GoTo(FlaskForm):
    year = StringField('Year')
    month = StringField('Month')
    submit = SubmitField('GoTo')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String)
    month = db.Column(db.String)
    day = db.Column(db.String)
    task = db.Column(db.Integer,default=0)
    def __init__(self,year,month,day,task):
        self.year = year
        self.month = month
        self.day = day
        self.task = task





@app.route('/', methods=['GET','POST'])
def index():
    datalist = []
    year = str(datetime.now().strftime("%Y"))
    month = str(datetime.now().strftime("%m"))
    x_home = str(year) + str(int(month))
    days = day_in_month(month,year)  
    form = GoTo()
    if request.method=='POST':
        try:
            # Insert new data
            data = decode_resp(request.data.decode('ascii'))
            db.session.add(Task(data['year'],data['month'],data['day'], 1))
            db.session.commit()
        except:
            # goto another month
            if form.validate_on_submit():
                year  = form.year.data 
                month = form.month.data 
            
    
    for day in range(1,days+1):
        x = Task.query.filter_by(day=day,month=str(int(month)),year=(year)).first()
        
        if x:
            datalist.append([day,x.task])
            
        else:
            
            datalist.append([day,0])
    
    y_home = str(year) + str(int(month))
    return render_template('calender.html', year=year, month=int(month), homebutton=(x_home==y_home) ,fullNameOfMonth=month_name(month),datalist=datalist, form=form, blank_divs=blank_divs(year,month))


if __name__ == "__main__":
    app.run(debug=True)