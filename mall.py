#this is my main server code
#COPYRIGHTED. DO NOT COPY.
#YOU WILL BE FINED $999,999,999,999,999 INSTANTLY

import cgi
import re
import pymongo
import bottle
from bson.objectid import ObjectId
from bottle import route,post,default_app,run,static_file,request
from bottle import mako_template as template
from datetime import datetime
from siteSettings import Site
from collections import namedtuple


hellostr= """<h1>Hello {}</h1>"""

@route('/static/<path:path>')
def static(path):
    return static_file(path,root=Site.staticRoot)

@bottle.route('/')
def main(folder='', path='index.html'):
    now=datetime.now().strftime('%A %d-%b-%Y %H:%M:%S')

    return template(path,time=now)

application = default_app()

XYZ=namedtuple('XYZ','x y z')

@bottle.route('/bourne/<store>')
def jsonTransver(store='central'):
    def dopos(string):
        if isinstance(string,list):
            return XYZ(*string)
        return XYZ(*[float(s) for s in string.split(',')])            
    def process(stock):
        def field(key,value):
            def tolist(string):
                if not string:
                    return ''
                return dopos(string)._asdict()
            
            mapfld={'pos':tolist}
            if key in mapfld:
                value = mapfld[key](value)
            return value

        keymap={'blenderFile':'shape','name':'Name'}
        exclude= "_id",
        
        res = { keymap.get(key,key):field(key,item) for key,item in stock.items() if key not in exclude}
        if not res['pos']:
            res['mode'] = 1
            del res['pos']
        #res['shape'] = res.get('blenderFile','')
        return res
    def sorter(item):
        return item['place']
    ans = [process(stock) for stock in database.stock.find({"shop":store})]
    #print('ans',ans)
    dups =[]
    for dup in ans:
        # loop for items to repreat
        if isinstance(dup,dict) and dup.get('repeat'):
            repeat= int(dup['repeat'])
            repos= dopos(dup['reappos'])
            pos=XYZ(**dup['pos'])
            #repos=XYZ( repos.x - pos.x , repos.y - pos.y ,repos.z - pos.z)
            #scale= 1 if not dup['scale'] else float(dup['scale'])
            loopscale=1 if not dup['reapscale'] else float(dup['reapscale'])
            scale=loopscale

            thispos=dup['pos'].copy()
            for count in range(repeat):
                ducopy=dup.copy()
                pos=XYZ( repos.x + pos.x , repos.y + pos.y ,repos.z + pos.z)
                ducopy['pos']=pos._asdict()
                if ducopy['scale']:
                    ducopy['scale']=float(ducopy['scale'])*loopscale
                    loopscale*=scale
                dups+=[ducopy]
    #print('dups',dups)    
    ans+=dups  #add in the repeats
        
    ans.sort(key=sorter)
    print(ans)
    return {"items":ans}
    

@bottle.route('/savefile')
def showsavefile():
    parms= dict(description='',name='',price='',gender='',
                blenderFile='',shop='',place="",pos="", scale="")
    return template('savefile.html',field_dict=parms) #**parms)
    
@bottle.post('/savefile')
def savefile():
    print('dir',request.method)
    form=request.forms
    print('form',form.keys())
    database.stock.insert(form)
    return showsavefile()

@bottle.route('/shops')
def showshopfile():
    shops = [shop for shop in database.stock.find().distinct("shop")]
    print("shops",shops)
    return template('shops.html',shops=shops)

@bottle.route('/items/<shop>')
def showitems(shop):
    stock = [stock for stock in database.stock.find({"shop":shop})]
    print("shops",stock)
    fields= ["name","place","price"]
    return template('stock.html',stock=stock,fields=fields)

@bottle.route('/edit/<_id>')
def showsaveedit(_id):
    read = database.stock.find_one({"_id":ObjectId(_id)})
    print(read)
    parms= dict(description='',name='',price='',gender='',
                blenderFile='',shop='',place="",pos="", scale="")
    return template('savefile.html',field_dict=read) #**parms)
    
@bottle.post('/edit/<_id>')
def saveedit(_id):
    print('dir',request.method)
    form=request.forms
    print('form',form.keys())
    database.stock.update({"_id":ObjectId(_id)},form)
    return showitems(form["shop"])

@bottle.route('/hello/<name>')
def show_name(name='(you have no name)'):
    return hellostr.format(name.capitalize())


if __name__ == '__main__':
    connection_string = "mongodb://localhost"
    connection = pymongo.MongoClient(connection_string)
    database = connection.mall
    run(port=8080,host="0.0.0.0",debug=True)