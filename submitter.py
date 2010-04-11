#!/usr/bin/env python3.0
import re
import http.client
from datetime import datetime
from xml.sax.saxutils import escape
from juno import init, redirect, route, run, get, \
                 model, post, get, find, session, \
                 subdirect, template, autotemplate
init({'static_url':'/s/*:file', '500_traceback':True, 'use_templates':True,
  'use_db':True, 'use_sessions':True,
  'template_kwargs':{'extensions':["jinja2.ext.do","jinja2.ext.loopcontrols"]}})

#constants

re_url = r'(?<!")((https?|ftp|gopher|file)://(\w|\.|/|\?|=|%|&|:|#|_|-)+)'
sections = [("Episodes","/radio"),
            ("Login","login"),
            ("Add a News","submit")]
header_color = "ffc8b4"
default = {'sections':sections, 'header_color':header_color}

#models

Entry = model('Entry',title='string',url='string',
                      description='text',excerpt='text',
                      date='datetime',score='integer'
             )# tags is a list of ids as string
Tag = model('Tag', title='string', category='integer')
Linker = model('Linker', entry='integer', tag='integer')#links between entries and tags
Category = model('Category', name='string')

# routes

autotemplate(['/','news'], "submitter.tpl",
  entries=lambda:[ (entry, Tag.find().filter(
                    Tag.id.in_(list(map(lambda t:t[0],
                    find(Linker.tag).filter_by(entry=entry.id).all() )))).all())
                    for entry in reversed(Entry.find().order_by(
                    Entry.date).limit(30).all()) ],
  css="submitter", **default)

@get('login')
def login(web):
  return template("login.tpl", **default)

@post('login')
def check(web):
  return template("login.tpl", **default)

@post('add')
def add_news(web):
  params = dict([ (key,escape(web.input(key).strip())) for key in ['title','url','description'] ])
  params['date'] = datetime.now()
  params['excerpt'] = re.sub(re_url,
         lambda x: '<a href="%s" class="link"><span class="domain">%s</span>%s</a>' % _parse_url(x.group()),
         escape(web.input('excerpt').strip()).replace("\n","<br/>"))
  entry = Entry(score=0, **params).save()
  tags = web.input('tags').split()
  if tags:
    known_tags = Tag.find().filter(Tag.title.in_(tags)).all()
    for tag in known_tags:
      tags.remove(tag.title)
      Linker(entry=entry.id, tag=tag.id).add()
    for tagtitle in tags:
      tag = Tag(title=tagtitle, category="").save()
      Linker(entry=entry.id, tag=tag.id).add()
    session().commit()
  return redirect("news")

@get('like')
def like_it(web):
  try: id = int(web['QUERY_STRING'])
  except: id = None
  if id is not None:
    Entry.find().filter_by(id=id).update({Entry.score: Entry.score+1})
    session().commit()
  return redirect('news')

@get('hate')
def like_it(web):
  try: id = int(web['QUERY_STRING'])
  except: id = None
  if id is not None:
    Entry.find().filter_by(id=id).update({Entry.score: Entry.score-1})
    session().commit()
  return redirect('news')

@route('submit')
def submit(web):
  kwargs = dict(default)
  if web.input('blob') is not None:
    blob = web.input('blob').strip()
    m = re.search(re_url,blob)
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

#helper

def _parse_url(url):
    domain = url.split(':',1)[1][2:].split('/',1)
    if len(domain) == 1: domain, rest = domain[0], ""
    else:
        domain, rest = domain
        if not rest == "": rest = '/'+rest
    if domain.startswith('www.'): domain = domain[4:]
    return (url, domain, rest)

# examples

Entry(title="test",url="http://localhost:8000/",description="yay! a test ..", excerpt="blub", score=0).save()

# run

run()

