#this is my main code
#COPYRIGHTED. DO NOT COPY.
#YOU WILL BE FINED $999,999,999,999,999 INSTANTLY

import cgi
import re
import pymongo
import bottle
from bottle import route,post,default_app,run,static_file,request
from bottle import mako_template as template
from datetime import datetime
from siteSettings import Site


hellostr= """<h1>Hello {}</h1>"""

@route('/static/<path:path>')
def static(path):
    return static_file(path,root=Site.staticRoot)

@bottle.route('/')
def main(folder='', path='index.html'):
    now=datetime.now().strftime('%A %d-%b-%Y %H:%M:%S')

    return template(path,time=now)

application = default_app()

@bottle.route('/savefile')
def showsavefile():
    parms= dict(description='',name='',price='',gender='',
                blenderFile='',shop='')
    return template('savefile.html',**parms)
    
@bottle.post('/savefile')
def savefile():
    print('dir',request.method)
    form=request.forms
    print('form',form.keys())
    database.clothes.insert(form)
    return showsavefile()

@bottle.route('/hello/<name>')
def show_name(name='(you have no name)'):
    return hellostr.format(name.capitalize())


if __name__ == '__main__':
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    database = connection.mall
    run(port=8080,host="0.0.0.0",debug=True)