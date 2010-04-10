#!/usr/bin/env python3.0
import re
import http.client
from datetime import datetime
from juno import init, redirect, route, run, get, \
                 model, post, get, find, \
                 subdirect, template, autotemplate
init({'static_url':'/s/*:file', '500_traceback':True, 'use_templates':True,
  'use_db':True, 'use_sessions':True,
  'template_kwargs':{'extensions':["jinja2.ext.do","jinja2.ext.loopcontrols"]}})

#constants

sections = [("Episodes","/radio"),
            ("Login","login"),
            ("Add a News","submit")]
header_color = "ffc8b4"
default = {'sections':sections, 'header_color':header_color}

#models

Entry = model('Entry',title='string',url='string',description='text',excerpt='text',tags='string',date='datetime')# tags is a list of ids as string
Tag = model('Tag', title='string', category='integer')
Category = model('Category', name='string')

# routes

autotemplate(['/','news'], "submitter.tpl",
  entries=lambda:reversed(Entry.find().order_by(Entry.date).limit(30).all()),
  css="submitter", **default)

@get('login')
def login(web):
  return template("login.tpl", **default)

@post('login')
def check(web):
  return template("login.tpl", **default)

@post('add')
def add_news(web):
  params = dict([ (key,web.input(key)) for key in ['title','url','description','excerpt'] ])
  params['date'], T = datetime.now(), find(Tag.id)
  params['tags'] = " ".join(map(str,[
         T.filter_by(title=tagtitle).scalar() or
         Tag(title=tagtitle, category="").save().id
           for tagtitle in web.input('tags').split() ]))
  Entry(**params).save()
  return redirect("news")
  #Entry()

@route('submit')
def submit(web):
  kwargs = dict(default)
  if web.input('blob') is not None:
    blob = web.input('blob').strip()
    m = re.match(r'(?<!")((https?|ftp|gopher|file)://(\w|\.|/|\?|=|%|&|:|_|-)+)',blob)
    if m:
      url = kwargs['url'] = m.group(0)
      if url.startswith("http:"):
        url = list(url[7:].partition("/"))
        domain, path, res = url.pop(0), "".join(url), None
        try:
          conn = http.client.HTTPConnection(*domain.split(":"), timeout=9)
          conn.request('GET', path)
          res = conn.getresponse()
        except: pass
        if res and res.status < 300:
          site = str(res.read(), 'utf-8')
          m = re.search(r"<title>(?P<title>.*)</title>", site)
          if m: kwargs['url_title'] = m.group('title')
    if 'url' not in kwargs or 'url' in kwargs and kwargs['url'] != blob:
      kwargs['excerpt'] = blob
  return template("submit.tpl", **kwargs)

# examples

Entry(title="test",url="http://localhost:8000/",description="yay! a test ..", excerpt="blub", tags="").save()

# run

run()

