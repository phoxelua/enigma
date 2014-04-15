from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash
from app import app
from Input import *
from DataSet import *
from Source import *
from Query import *
import os
import sqlite3



#Lol global variables
SOURCES = [BEASource()] #add more sources


@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    # assume country is murica and region == state
    box1 = request.form['data1']
    box2 = request.form['data2']
    start = request.form['start']
    end = request.form['end'] 

    print "Forms Read: "
    print box1
    print box2
    print start, end
    
    uinput = Input(box1, box2, start, end)

    # uinput = Input("US corporateprofit", "US gdp", "1933", "2010")
    q1, q2 = uinput.generateQueries(SOURCES)
    print "Q1: " + q1.toString()
    print "Q2: " + q2.toString()
    d1 = DataSet(q1.source.makeDictionary(q1))
    d2 = DataSet(q2.source.makeDictionary(q2))


    # dat1 = {"1990": 1000000000, "1991": 2000000000, "1992": 3000000000, "1993":4000000000, "1994": 5000000000, "1995":6000000000, "1996":7000000000, "1997":8000000000, "1998":9000000000, \
    #         "1999":10000000000, "2000":11000000000, "2001":12000000000, "2002":13000000000}
    # dat2 = {"1990": 2000000000, "1991": 4000000000, "1992": 6000000000, "1993":9000000000, "1994": 9000000000, "1995":13000000000, "1996":14000000000, "1997":16000000000, "1998":18000000000, \
    #         "1999":20000000000, "2000":21000000000, "2001":22000000000, "2002":26000000000}
    # dat1 = {"1990": 1, "1991": 2, "1992": 3, "1993":4, "1994": 5, "1995":6, "1996":7, "1997":8, "1998":9, \
    #         "1999":10, "2000":11, "2001":12, "2002":13}
    # dat2 = {"1990": 2, "1991": 4, "1992": 6, "1993":9, "1994": 9, "1995":13, "1996":14, "1997":16, "1998":18, \
    #         "1999":20, "2000":21, "2001":22, "2002":26}
    # d1 = DataSet(dat1)
    # d2 = DataSet(dat2)



    m, b, r, p, stderr = d1.linearRegression(d2)
    r = d1.calcR(d2)[0]
    r = '%.3f'%(r)
    d1v = d1.data.values()
    d2v = d2.data.values()

    # #lol
    n1 = box1
    n2 = box2

    c = max(len(str(d1v)),len(str(d2v)))
    print m, b, r, p, stderr

    # return render_template('index.html')
    return render_template('display.html', data1=d1v, name1=n1, data2=d2v,  name2=n2, R=r, m=m, b=b, c=c)

@app.route('/display', methods=['GET','POST'])
def display():
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

    # data1 = {"1990": 1, "1991": 2, "1992": 3, "1993":4, "1994": 5, "1995":6, "1996":7, "1997":8, "1998":9, \
    #         "1999":10, "2000":11, "2001":12, "2002":13}
    # data2 = {"1990": 2, "1991": 4, "1992": 6, "1993":9, "1994": 9, "1995":13, "1996":14, "1997":16, "1998":18, \
    #         "1999":20, "2000":21, "2001":22, "2002":26}
    # start = "1990"
    # end = "2002" 

    # # assume country is murica and region == state
    # dataregion1, datatype1  = request.form['data1'].split(" ")
    # dataregion2, datatype2 = request.form['data2'].split(" ")
    # start = request.form['start']
    # end = request.form['end']
    # print start, end
    # print dataregion1
    # print datatype1
    # print datatype2
    # print dataregion2

    # uinput = Input(datatype1, datatype2, "murica", "murica", dataregion1, dataregion2, None, None, start, end)
    # # # uinput = Input(data1 ,data2, country1, country2, state1, state2, county1, county2, start, end)
    # d1 = DataSet(uinput.makeDictionary(1))
    # d2 = DataSet(uinput.makeDictionary(2))

    # data1 = {"1990": 1, "1991": 2, "1992": 3, "1993":4, "1994": 5, "1995":6, "1996":7, "1997":8, "1998":9, \
    #         "1999":10, "2000":11, "2001":12, "2002":13}
    # data2 = {"1990": 2, "1991": 4, "1992": 6, "1993":9, "1994": 9, "1995":13, "1996":14, "1997":16, "1998":18, \
    #         "1999":20, "2000":21, "2001":22, "2002":26}
    # start = "1990"
    # end = "2002"

    # d1 = DataSet(data1)
    # d2 = DataSet(data2)
    # global m, b, r, p, stderr
    m, b, r, p, stderr = d1.linearRegression(d2)
    r = d1.calcR(d2)[0]
    r = '%.3f'%(r)
    # global d1v, d2v
    d1v = d1.data.values()
    d2v = d2.data.values()
    # global n1, n2
    n1 = datatype1
    n2 = datatype2
    print "in display"
    return render_template('display.html', data1=d1v, name1=n1, data2=d2v,  name2=n2, R=r, m=m, b=b)


@app.route('/chart', methods=['GET','POST'])
def chart():
    # global m, b, r, p, stderr, d1v, d2v
    return render_template('chart.html', data1=d1v, name1=n1, data2=d2v,  name2=n2, R=r, m=m, b=b)
