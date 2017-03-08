# -*- coding: utf-8 -*-
import ujson, os, urllib2, platform
from flask import Flask, render_template, request
app = Flask(__name__)

def PlatformHostsSwitch():
    def attachHosts(file, comment, hosts):
        fp = open(file, 'a+b')
        if hosts not in fp.read():
        	fp.write(comment + hosts)
        fp.close()
    
    sysstr = platform.system()
    if(sysstr =="Windows"):
        attachHosts(
        	'C:\\Windows\\System32\\drivers\\etc\\hosts',
        	'\r\n#google===========================\r\n',
        	'127.0.0.1 www.renren.com'
        )
    elif(sysstr == "Linux"):
        attachHosts(
        	'/etc/hosts',
        	'\n#google===========================\n',
        	'127.0.0.1 www.renren.com'
        )

PlatformHostsSwitch()


NAMES_FILE = '.cache/names.json'

with open(NAMES_FILE) as f:
    names = map(lambda x:ujson.loads(x), [x for x in f.read().split("\n") if x])

@app.route('/')
def profiles():
    name = request.args.get('name')
    name = name if name else ''
    if name:
    	items = [x for x in names if x['name'].find(name) >= 0]
    else:
    	items = names
    return render_template('profiles.html', names=items, name=name)

if __name__ == '__main__':
    app.run()
