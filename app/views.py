from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash
from app import app
from Input import *
from DataSet import *
import os
import sqlite3



#Lol global variables
d1v = None
d2v = None
m = 0
b = 0
r = 0
p = 0
stderr = 0
n1 = ""
n2 = ""

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    # # assume country is murica and region == state
    dataregion1, datatype1  = request.form['data1'].split(" ")
    dataregion2, datatype2 = request.form['data2'].split(" ")
    start = request.form['start']
    end = request.form['end'] 
    print start, end
    print dataregion1
    print datatype1
    print datatype2
    print dataregion2
    
    uinput = Input(datatype1, datatype2, "murica", "murica", dataregion1, dataregion2, None, None, start, end)
    # # uinput = Input(data1 ,data2, country1, country2, state1, state2, county1, county2, start, end)
    d1 = DataSet(uinput.makeDictionary(1))
    d2 = DataSet(uinput.makeDictionary(2))
    # r = d1.calcR(d2)
    # m, b, r, p, stderr = d1.linearRegression(d2)

    # data1 = {"1990": 1, "1991": 2, "1992": 3, "1993":4, "1994": 5, "1995":6, "1996":7, "1997":8, "1998":9, \
    #         "1999":10, "2000":11, "2001":12, "2002":13}
    # data2 = {"1990": 2, "1991": 4, "1992": 6, "1993":9, "1994": 9, "1995":13, "1996":14, "1997":16, "1998":18, \
    #         "1999":20, "2000":21, "2001":22, "2002":26}
    # start = "1990"
    # end = "2002" 

    # d1 = DataSet(data1)
    # d2 = DataSet(data2)
    global m, b, r, p, stderr
    m, b, r, p, stderr = d1.linearRegression(d2)
    r = d1.calcR(d2)[0]
    global d1v, d2v
    d1v = d1.data.values()
    d2v = d2.data.values()
    global n1, n2
    n1 = "hackathons"
    n2 = "obesity"

    return render_template('index.html')

@app.route('/chart', methods=['GET','POST'])
def chart():
    # global m, b, r, p, stderr, d1v, d2v
    return render_template('chart.html', data1=d1v, name1=n1, data2=d2v,  name2=n2, R=r, m=m, b=b)
    # return render_template('chart.html', data1=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], data2=[11, 10, 2, 7, 5, 21, 1, 2, 8, 9, 1, 5, 1], R=r, m=2.01, b=4.98)
