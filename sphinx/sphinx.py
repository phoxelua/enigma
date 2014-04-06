# all the imports
from Input import *
from DataSet import *
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


#Lol global variables
d1 = None
d2 = None
uinput = None
r = 0

# globals for testing
data1 = [1,2,3,4]
data2 = [1,1,1,1]
r = .001

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    #DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/chart')
# def chart():
#     return render_template('chart.html')



@app.route('/', methods=['POST'])
def my_form_post():
    data1 = request.form['data1']
    data2 = request.form['data2']
    start = request.form['start']
    end = request.form['end'] 
    print start, end
    print data1, data2
    # uinput = Input(query1, query2, query3)
    # # uinput = Input(data1 ,data2, country1, country2, state1, state2, county1, county2, start, end)
    # d1 = DataSet(uinput.makeDictionary(1))
    # d2 = DataSet(uinput.makeDictionary(2))
    # r = d1.calcR(d2)


    # return render_template('chart.html', data1=d1.data.values(), data2=d2.data.values(), R=r)
    # return render_template('chart.html', data1=[1,2,3,4], data2=[1,1,1,1], R=.001)
    return render_template('index.html', data1=data1, data2=data2, start=start, end=end)

@app.route('/chart', methods=['GET','POST'])
def chart():
    return render_template('chart.html', data1=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], data2=[11, 10, 2, 7, 5, 21, 1, 2, 8, 9, 1, 5, 1], R=r, m=2, b=4)


if __name__ == '__main__':
    app.run()
