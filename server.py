#!/usr/bin/env python3.0
import re
from time import time
from hashlib import sha1
from markdown import Markdown
from random import randint, random, shuffle
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor
from datetime import datetime # year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None
from juno import init, redirect, route, run, model, post, template, find, \
                  get, yield_file#, \
#                 open_nutshell, close_nutshell, getHub, subdirect

# init

init({'static_url':      '/(s/)?(?P<file>(?<=s/).*|(css|img)/.*)',
      '500_traceback':   True,
      'use_templates':   True,
      'bind_address':    '',
      'use_db':          True,
      'db_location':     "db.sqlite",
      'template_kwargs':
         {'extensions':  ["jinja2.ext.do","jinja2.ext.loopcontrols"]}
     })

from db import *

# import submitter

#open_nutshell()
#import submitter
#submitter = getHub()
#close_nutshell()

# constants

re_reply    = re.compile(
                         r'@(\w+)'
                        )
re_url      = re.compile(
 r'(?<!"|\()((https?|ftp|gopher|file)://(\w|\.|/|\(|\)|\?|=|%|&|:|#|_|-|~|\+)+)'
                        )
re_anchor   = re.compile(
r'(<\s*a[^<>]*)(>(?!(https?|ftp|gopher|file)://)(.(?!<\s*/\s*a\s*>))*.<\s*/\s*a\s*>)'
                        )
#head_colors = {'radio': "ffc8b4",
#               'cast':  "b4c8ff",
#               'music': "c8ffc8"
#              }
#sections = {'radio': [],#[("Pentasubmitter","/radio/submitter/")],
#            'cast':  [],
#            'music': []
#           }

# cache

comment_hashes = {}

# markdown stuff

class LinkPreprocessor(Preprocessor):
  def run(self, lines):
    def parse(x): return "[{0}]({0})".format(x.group())
    def sub(line): return re_url.sub(parse, line)
    return list(map(sub, lines))

class LinkPostprocessor(Postprocessor):
  def run(self, text):
    def parse(x): return '<span class="line">{1}</span>{2}'.\
                         format(*_parse_url(x.group()))
    def classify(x): return '{0} class="line"{1}'.format(*x.groups())
    text = re_anchor.sub(classify, text)
    return re_url.sub(parse, text)

md = Markdown(
              safe_mode     = 'escape',
              output_format = 'xhtml1'
             )

md.preprocessors.add("url", LinkPreprocessor(md), "_begin")
md.postprocessors.add("url", LinkPostprocessor(md), "_end")

# routes

@route("/")
def start(web): # FIXME wrap db queries into one
  episodes = {}
  for category in ['pentaradio','pentamusic','pentacast']:
    episode = list(reversed(Episode.find().\
                   filter_by(category=category).\
                   order_by(Episode.date).\
                   all()
                  ))
    if len(episode) > 13:
      episode = episode[:13]
      episode.append({'name': "more …", 'link': ""})
    episodes[category] = episode
  return template("start.html",
                  episodes = episodes,
                  css      = "start"
                 )


@post("/(?P<site>pentaradio|pentacast|pentamusic)/:id/comment/new")
def new_comment(web, site, id):
  try:    episode = Episode.find().filter_by(link = id).one()
  except: return redirect("/{0}".format(site))
  found, hash, now = False, web.input('hash'), time()
  captcha, tip = web.input('tcha'), None
  if captcha == "sum":
    typ, tip = 1, web.input('sumtcha')
    try:    tip = int(tip)
    except: tip = None
  elif captcha == "cat":
    typ, tip = 2, web.input('cat')
    if not isinstance(tip, list): tip = [tip]
  else:
    typ, tip = 0, -1
  if hash is not None:
    if hash in comment_hashes:
      found = comment_hashes[hash][typ] == tip
      del comment_hashes[hash]
  for comment_try in list(comment_hashes.keys()):
    if now - comment_hashes[comment_try][0] > 10400: # 12 hours
      del comment_hashes[comment_try]
  if found and \
     web.input('author')  is not None and \
     web.input('comment') is not None and \
     web.input('reply')   is not None and \
     web.input('comment') != "":
    text, reply = md.convert(web.input('comment')), []
    def replyer(x):
      a = x.group()[1:]
      i = find(Comment.id).filter_by(author=a).order_by(Comment.date).all()
      if i: reply.append(i[-1][0])
      return i and '@<a href="/{0}/{1}/reply?{2}#new">{3}</a>'.\
                   format(site, id, i[-1][0], a)\
                or "@{0}".format(a)
    text = re_reply.sub(replyer, text)
    if reply: reply = reply[0]
    else:     reply = -1
    if web.input('reply') != "-1":
      try: reply = int(web.input('reply'))
      except: pass
    Comment(episode = episode.id,
            author  = web.input('author'),
            reply   = reply,
            text    = text,
            date    = datetime.now()
           ).save()
  return redirect("/{0}/{1}".format(site,id))


@get("/cat/(?P<typ>[A-Z])")
def cat_image(web, typ):
    try:
      hash = web['QUERY_STRING']
      iscat = typ in comment_hashes[hash][2]
      nr = comment_hashes[hash][3][ord(typ)-65]
    except: return
    yield_file("static/img/{0}acat{1}.jpeg".\
      format(not iscat and "not" or "", nr))



#@route(['radio/submitter', 'radio/submitter/:rest'])
#def submitter_site(web, rest = ""):
#  return subdirect(web, submitter, rest)


@route("/(?P<site>pentaradio|pentacast|pentamusic)/(?P<id>[^/]*)(?P<cmnt>/(comment|reply))?")
def episode(web, site, id, cmnt):
  try: # FIXME wrap db queries into one
    episode  = Episode.find().filter_by(link = id).one()
    files    = File.find().filter_by(episode = episode.id).all()
    links    = Link.find().filter_by(episode = episode.id).all()
    comments = Comment.find().filter_by(episode = episode.id).\
                 order_by(Comment.date).all()
  except: return redirect("/{0}".format(site))
  comments, reply, author, hash, a, b, c = do_the_comments(web, comments, cmnt)
  return template("episode.tpl",
                  #header_color = head_colors[site],
                  comment_form = cmnt is not None,
                  css          = "episode",
                  episode      = episode,
                  site         = site,
                  comments     = comments,
                  files        = files,
                  links        = links,
                  #sections     = sections[site],
                  reply        = reply,
                  at_author    = author,
                  hash         = hash,
                  a = a, b = b, c = c
                 )


@route("/(?P<site>pentaradio|pentacast|pentamusic)/(?P<id>[^/]*)/comments(?P<cmnt>/(comment|reply))?")
def comments(web, site, id, cmnt):
  try: # FIXME wrap db queries into one
    episode  = Episode.find().filter_by(link = id).one()
    comments = Comment.find().filter_by(episode = episode.id).\
                 order_by(Comment.date).all()
  except: return template("comments.tpl", fail = True)
  comments, reply, author, hash, a, b, c = do_the_comments(web, comments, cmnt)
  return template("comments.tpl",
                  #header_color = head_colors[site],
                  comment_form = cmnt is not None,
                  css          = "episode",
                  episode      = episode,
                  site         = site,
                  comments     = comments,
                  reply        = reply,
                  at_author    = author,
                  hash         = hash,
                  a = a, b = b, c = c
                 )


@route("/(?P<filename>(pentaradio24|pentacast|pentamusic)-.*)/comments(?P<cmnt>/(comment|reply))?")
def comments_by_filename(web, filename, cmnt):
  filename = "content/news/{0}.xml".format(filename)
  try: # FIXME wrap db queries into one
    episode  = Episode.find().filter_by(filename = filename).one()
    comments = Comment.find().filter_by(episode = episode.id).\
                 order_by(Comment.date).all()
    if   "radio" in filename: site = "pentaradio"
    elif "cast"  in filename: site = "pentacast"
    elif "music" in filename: site = "pentamusic"
    else: site = 42 / 0
  except: return template("comments.tpl", fail = True)
  comments, reply, author, hash, a, b, c = do_the_comments(web, comments, cmnt)
  return template("comments.tpl",
                  #header_color = head_colors[site],
                  comment_form = cmnt is not None,
                  css          = "episode",
                  episode      = episode,
                  site         = site,
                  comments     = comments,
                  reply        = reply,
                  at_author    = author,
                  hash         = hash,
                  a = a, b = b, c = c
                 )


@route("/(?P<site>pentaradio|pentacast|pentamusic)/")
def main(web, site):
  episodes = Episode.find().filter_by(category=site).\
               order_by(Episode.date).all()
  episodes.reverse()
  # FIXME wrap db queries into one
  comments_count = [ Comment.find().filter_by(episode = e.id).count()
                     for e in episodes ]
  return template("episodes.tpl",
                  #header_color= head_colors[site],
                  css         = "episode",
                  episodepage = zip(episodes, comments_count),
                  site        = site#,
                  #sections    = sections[site]
                 )

# helper

def _parse_url(url):
    domain = url.split(':',1)[1][2:].split('/',1)
    if len(domain) == 1: domain, rest = domain[0], ""
    else:
        domain, rest = domain
        if not rest == "": rest = "/{0}".format(rest)
    if domain.startswith('www.'): domain = domain[4:]
    return (url, domain, rest)


def do_the_comments(web, comments, mode):
  replying, idcomments = {}, {}
  for comment in list(comments):
    comment.level, idcomments[comment.id] = 0, comment
    r = comment.reply
    if r != -1:
      comments.remove(comment)
      if not r in replying:
        replying[r] = []
      replying[r].append(comment)
  level_replying = sum(replying.values(),[])
  while replying: # ups .. what a crapy code
    stash = []
    for comment in comments:
      stash.append(comment)
      if comment.id in replying:
        stash += replying[comment.id]
        del replying[comment.id]
    comments = stash
  for reply in level_replying:
    cur = reply
    while cur.reply != -1:
      reply.level += 1
      cur = idcomments[cur.reply]
  try:
    reply = int(web['QUERY_STRING'])
    author = find(Comment.author).filter_by(id = reply).one()[0]
    author = "@{0} ".format(author)
  except: reply, author = -1, ""
  a, b, c = randint(1, 10), randint(1, 10), randint(1, 10)
  hash = sha1(bytes(str(random()),'utf-8')).hexdigest()
  if mode:
    cats = [ chr(65+i) for i in range(4) if randint(0, 1) ]
    if not len(cats): cats = [chr(65+randint(0, 4))]
    elif len(cats) == 4: cats.pop(randint(0, 4))
    pics = list(range(16)); shuffle(pics); pics = pics[:4]
    comment_hashes[hash] = (time(), a + b + c, cats, pics)
  return comments, reply, author, hash, a, b, c

# run

run()

