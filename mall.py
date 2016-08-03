#this is my main server code
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

@bottle.route('/bourne/<store>')
def jsonTransver(store='central'):
    def process(stock):
        def field(key,value):
            def tolist(string):
                if not isinstance(string,list):
                    string = [float(s) for s in string.split(',')]
                return {'x':string[0],'y':string[1],'z':string[2]}
            mapfld={'pos':tolist}
            if key in mapfld:
                value = mapfld[key](value)
            return value

        keymap={'blenderFile':'shape','name':'Name'}
        exclude= "_id",
        
        res = { keymap.get(key,key):field(key,item) for key,item in stock.items() if key not in exclude}
        #res['shape'] = res.get('blenderFile','')
        return res
    ans = [process(stock) for stock in database.stock.find({"shop":store})]
    print(ans)
    return {"items":ans}
    

@bottle.route('/savefile')
def showsavefile():
    parms= dict(description='',name='',price='',gender='',
                blenderFile='',shop='',place="",pos="")
    return template('savefile.html',**parms)
    
@bottle.post('/savefile')
def savefile():
    print('dir',request.method)
    form=request.forms
    print('form',form.keys())
    database.stock.insert(form)
    return showsavefile()

@bottle.route('/hello/<name>')
def show_name(name='(you have no name)'):
    return hellostr.format(name.capitalize())


if __name__ == '__main__':
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    database = connection.mall
    run(port=8080,host="0.0.0.0",debug=True)