#!/usr/bin/env python3.0
import re
import http.client
from datetime import datetime
from xml.sax.saxutils import escape, unescape
from juno import init, redirect, route, run, get, \
                 model, post, get, find, session, \
                 subdirect, template, autotemplate
 
# init

init({'static_url':      '/s/*:file',
      '500_traceback':   True,
      'use_templates':   True,
      'use_db':          True,
      'use_sessions':    True,
      'template_kwargs':
         {'extensions':  ["jinja2.ext.do","jinja2.ext.loopcontrols"]}
     })

# constants

re_url       = r'(?<!")((https?|ftp|gopher|file)://(\w|\.|/|\?|=|%|&|:|#|_|-|\+)+)'
re_anchor    = r'''<\s*a[^<>]*?href\s*=\s*["'](?P<url>[^"'>]*)["'](.(?!<\s*/\s*a\s*>))*.<\s*/\s*a\s*>'''
re_url       = re.compile(re_url)
re_anchor    = re.compile(re_anchor)

sections     = [("Episodes",   "/radio"),
                ("News",       "news"),
                ("Login",      "login"),
                ("Add a News", "submit")
               ]
header_color = "ffc8b4"
default = {'sections':     sections,
           'header_color': header_color
          }

# models

Entry = model('Entry',
              title       = 'string',
              url         = 'string',
              description = 'text',
              excerpt     = 'text',
              date        = 'datetime',
              score       = 'integer'
             ) # tags is a list of ids as string
Tag = model('Tag',
            title    = 'string',
            category = 'integer'
           )
Linker = model('Linker',
               entry = 'integer',
               tag   = 'integer'
              ) # links between entries and tags
Category = model('Category',
                 name = 'string'
                )

# routes

@route(['/','news'])
def index(web): # FIXME reduce queries
  db_entries, news = Entry.find().order_by(Entry.date).limit(30).all(), []
  for entry in reversed(db_entries):
    tags = find(Linker.tag).filter_by(entry=entry.id).all()
    if tags:
      tags = list(map(lambda t:t[0], tags))
      tags = Tag.find().filter(Tag.id.in_(tags)).all()
      news.append( (entry, tags) )
    else: news.append( (entry, []) )
  cloud = Tag.find().limit(99).all() # FIXME sort by tag using count
  return template("submitter.tpl",
                  news  = news,
                  cloud = cloud,
                  css   = "submitter",
                 **default)


@get('login')
def login(web):
  return template("login.tpl", **default)


@post('login')
def check(web):
  return template("login.tpl", **default)


@post('add')
def add_news(web):
  params = dict([ ( key , escape(web.input(key).strip()) )
                  for key in ['title', 'url', 'description'] ])
  params['date']    = datetime.now()
  params['excerpt'] = re_url.sub(_iter_parse_url,
                             escape(web.input('excerpt').strip()).\
                             replace("\n","<br/>"))
  entry = Entry(score = 0, **params).save()
  tags  = web.input('tags').split()
  if tags:
    known_tags = Tag.find().filter(Tag.title.in_(tags)).all()
    for tag in known_tags:
      tags.remove(tag.title)
      Linker(entry = entry.id, tag = tag.id).add()
    for tagtitle in tags:
      tag = Tag(title = tagtitle, category = "").save()
      Linker(entry = entry.id, tag = tag.id).add()
    session().commit()
  return redirect("news")


@post('update')
def update_news(web):
  id = web.input('id')
  if id is not None:
    params = dict([ ( key , escape(web.input(key).strip()) )
                    for key in ['title', 'url', 'description'] ])
    params['date']    = datetime.now()
    params['excerpt'] = re_url.sub(_iter_parse_url,
                               escape(web.input('excerpt').strip()).\
                               replace("\n","<br/>"))
    entry = Entry.find().filter_by(id = id).update(params)
    tags  = web.input('tags').split()
    if tags:
      # FIXME remove unused tags
      Linker.find().filter_by(entry = id).delete()
      known_tags = Tag.find().filter(Tag.title.in_(tags)).all()
      for tag in known_tags:
        tags.remove(tag.title)
        Linker(entry = entry.id, tag = tag.id).add()
      for tagtitle in tags:
        tag = Tag(title = tagtitle, category = "").save()
        Linker(entry = id, tag = tag.id).add()
    session().commit()
  tag = web.input('tag')
  return redirect(tag and 'tag?{0}'.format(tag) or 'news')


@get('like')
def like_it(web):
  return __it(web, {Entry.score: Entry.score + 1})


@get('hate')
def like_it(web):
  return __it(web, {Entry.score: Entry.score - 1})


@route('tag')
def filter_by_tag(web):
  query_string, tag = web['QUERY_STRING'], None
  if query_string:
    try:    tag = Tag.find().filter_by(title = query_string).one()
    except: pass
    if tag:
      # FIXME wrap queries into one
      tags = list(map(lambda e:e[0],find(Linker.entry).filter_by(tag=tag.id).all()))
      db_entries, news = Entry.find().filter(Entry.id.in_(tags)).order_by(Entry.date).all(), []
      for entry in reversed(db_entries):
        tags = find(Linker.tag).filter_by(entry=entry.id).all()
        if tags:
          tags = list(map(lambda t:t[0], tags))
          tags = Tag.find().filter(Tag.id.in_(tags)).all()
          news.append( (entry, tags) )
        else: news.append( (entry, []) )
      cloud = Tag.find().limit(99).all() # FIXME sort by tag using count
      return template("submitter.tpl",
                      news  = news,
                      cloud = cloud,
                      css   = "submitter",
                      tag   = tag,
                     **default)
  return redirect('news')


@route('submit')
def submit(web):
  kwargs = dict(default)
  if web.input('blob') is not None:
    blob = web.input('blob').strip()
    m    = re_url.search(blob)
    if m:
      url = kwargs['url'] = m.group(0)
      if url.startswith("http:"):
        url = list(url[7:].partition("/"))
        domain, path, res = url.pop(0), "".join(url), None
        try:
          conn = http.client.HTTPConnection(*domain.split(":"), timeout = 9)
          conn.request('GET', path)
          res = conn.getresponse()
        except: pass
        if res and res.status < 300:
          site = str(res.read(), 'utf-8')
          m = re.search(r"<title>(?P<title>.*)</title>", site)
          if m: kwargs['url_title'] = m.group('title')
    if 'url' not in kwargs or 'url' in kwargs and kwargs['url'] != blob:
      kwargs['excerpt'] = blob
  return template("submit.tpl",
                  action = "add",
                 **kwargs)


@route('edit')
def edit(web):
  try:    id, tag = int(web['QUERY_STRING']), None
  except: id, tag = web.input('id'), web.input('tag')
  if id is not None:
    try:    entry = Entry.find().filter_by(id = id).one()
    except: entry = None
    if entry is not None:
      tags = find(Linker.tag).filter_by(entry = entry.id).all()
      if tags:
        tags = list(map(lambda t:t[0], tags))
        tags = find(Tag.title).filter(Tag.id.in_(tags)).all()
        tags = list(map(lambda t:t[0], tags))
      else: tags = []
      kwargs = dict(default)
      kwargs["tags"] = " ".join(tags)
      kwargs["url_title"]   = unescape(entry.title)
      kwargs["url"]         = unescape(entry.url)
      kwargs["description"] = unescape(entry.description)
      kwargs["excerpt"]     = re_anchor.sub(lambda x: x.group('url'), entry.excerpt)
      return template("submit.tpl",
                      action   = "update",
                      entry_id = id,
                      tag      = tag,
                     **kwargs)
  return redirect(tag and 'tag?{0}'.format(tag) or 'news')

# helper


def _iter_parse_url(x):
  return '<a href="{0}" class="link"><span class="domain">{1}</span>{2}</a>'.\
           format(*_parse_url(x.group()))

def _parse_url(url):
    domain = url.split(':',1)[1][2:].split('/',1)
    if len(domain) == 1: domain, rest = domain[0], ""
    else:
        domain, rest = domain
        if not rest == "": rest = "/{0}".format(rest)
    if domain.startswith('www.'): domain = domain[4:]
    return (url, domain, rest)


def __it(web, operator):
  try:    id, tag = int(web['QUERY_STRING']), None
  except: id, tag = web.input('id'), web.input('tag')
  if id is not None:
    Entry.find().filter_by(id = id).update(operator)
    session().commit()
  return redirect(tag and 'tag?{0}'.format(tag) or 'news')

# examples

Entry(title="test",url="http://localhost:8000/",description="yay! a test ..", excerpt="blub", score=0).save()

# run

run()

