#!/usr/bin/env python3.0
import re
from time import time
from hashlib import sha1
from markdown import Markdown
from random import randint, random
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor
from datetime import datetime # year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None
from juno import init, redirect, route, run, model, post, template, find#, \
#                 open_nutshell, close_nutshell, getHub, subdirect

# init

init({'static_url':      '/(s/)?(?P<file>(?<=s/).*|(css|img)/.*)',
      '500_traceback':   True,
      'use_templates':   True,
      'bind_address':    '',
      'use_db':          True,
      'template_kwargs':
         {'extensions':  ["jinja2.ext.do","jinja2.ext.loopcontrols"]}
     })

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

# models

File = model('File',
             episode = 'integer',
             info    = 'string',
             name    = 'string',
             type    = 'string',
             link    = 'string'
            )
Link = model('Link',
             episode = 'integer',
             title   = 'string',
             url     = 'string'
            )
Episode = model('Episode',
                name     = 'string',
                link     = 'string',
                category = 'string',
                author   = 'string',
                date     = 'datetime',
                fdate    = lambda self: _fdate(self.date),
                short    = 'text',
                long     = 'text'
               )
Comment = model('Comment',
                episode = 'integer',
                author  = 'string',
                reply   = 'integer',
                date    = 'datetime',
                fdate    = lambda self: _fdate(self.date),
                text    = 'text'
               )
# routes

@route("/")
def start(web): # FIXME wrap db queries into one
  episodes = dict([(c, reversed(Episode.find().\
                    filter_by(category=c).\
                    order_by(Episode.date).\
                    limit(13).all()))
                   for c in ['pentaradio','pentamusic','pentacast'] ])
  return template("start.html",
                  episodes = episodes,
                  css      = "start"
                 )


@post("/(?P<site>pentaradio|pentacast|pentamusic)/:id/comment/new")
def new_comment(web, site, id):
  try:    episode = Episode.find().filter_by(link = id).one()
  except: return redirect("/{0}".format(site))
  found, hash, captcha, now = False, web.input('hash'), web.input('captcha'), time()
  try:    captcha = int(captcha)
  except: captcha = None
  if hash is not None and captcha is not None:
    if hash in comment_hashes:
      found = comment_hashes[hash][1] == captcha
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
  replying = {}
  for comment in list(comments):
    r = comment.reply
    if r != -1:
      comments.remove(comment)
      if not r in replying:
        replying[r] = []
      replying[r].append(comment)
  while replying: # ups .. what a crapy code
    stash = []
    for comment in comments:
      stash.append(comment)
      if comment.id in replying:
        stash += replying[comment.id]
        del replying[comment.id]
    comments = stash
  try:
    reply = int(web['QUERY_STRING'])
    author = find(Comment.author).filter_by(id = reply).one()[0]
    author = "@{0} ".format(author)
  except: reply, author = -1, ""
  a, b, c = randint(1, 10), randint(1, 10), randint(1, 10)
  hash = sha1(bytes(str(random()),'utf-8')).hexdigest()
  if cmnt: comment_hashes[hash] = (time(), a + b + c)
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


@route("/(?P<site>pentaradio|pentacast|pentamusic)/")
def main(web, site):
  episodes = Episode.find().filter_by(category=site).\
               order_by(Episode.date).limit(20).all()
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

def _fdate(date:datetime):
  return date.strftime("%A, %d. %B %Y um %H:%M")

# example content

short = "Die Bundesrepublik - unendliche Bürokratie. Dies ist der Versuch des Pentacast etwas Licht ins Dunkel zu bringen."
long = "In dieser überaus spannenden und hitzigen Episode werden grundlegende Strukturen und Begriffe erklärt, die man für das Verständnis eines Rechtsstaates benötigt. Accuso, ein Volljurist aus dem Vereinsumfeld, steht Rede und Antwort und gibt ein paar aufschlussreiche Tips die dem Laien das Dickicht der Bürokratie und Juristerei algorithmisch zu durchdringen."
e = Episode(name="Rechtsstaat", category="pentacast", link="10", author="kl0bs", date=datetime(2010,4,4,16,14), short=short, long=long)
e.save()
File(episode=e.id, info="Ogg Vorbis, 94.1 MB", name="Pentacast 10: Rechtsstaat", link="http://ftp.c3d2.de/pentacast/pentacast-10-rechtsstaat.ogg", type="ogg").save()
File(episode=e.id, info="MPEG-Audio, 190.8 MB", name="Pentacast 10: Rechtsstaat", link="http://ftp.c3d2.de/pentacast/pentacast-10-rechtsstaat.mp3", type="mp3").save()

short = "Datenbanken sind die Leitz-Ordner der Rechenmaschinen. In ihnen wird versenkt, was man evtl. noch mal brauchen könnte. Daraus leiten sich zwei Probleme ab: Wie findet man diese Daten wieder und wie schnell kommt man wieder heran? Diese Probleme zu lösen haben relationale Datenbanksysteme über Jahrzehnte optimiert."
long = "Im Scope des Internets wird gleich ein 3. Problem offensichtlich: Wie viele Clients kommen quasi gleichzeitig an diese Daten ran? Wie schnell puhlt z. B. eine Suchmaschine die URL aus dem herunter geladenen Internet? <br/> Neue Lösungen sind also für die Datenhalden unserer Zeit gefragt. Wir reden mal etwas darüber, welche Ansätze es da so gibt, wie die Entwicklungen sind und geben Tipps, was Ihr auch mal in der eigenen Küche ausprobieren könnt. <br/> Ihr seid herzlich eingeladen anzurufen (0351/32 05 47 11) oder im c3d2 Channel mit uns zu chatten."
e = Episode(name="No, No, NoSQL, oder doch?", category="pentaradio", link="032010", author="a8", date=datetime(2010,3,23,13,28), short=short, long=long)  
e.save()
File(episode=e.id, info="Ogg Vorbis, 111.2 MB", name="pentaradio24 vom 23. März 2010", link="http://ftp.c3d2.de/pentaradio/pentaradio-2010-03-23.ogg", type="ogg").save()
File(episode=e.id, info="MPEG-Audio, 94.9 MB", name="pentaradio24 vom 23. März 2010", link="http://ftp.c3d2.de/pentaradio/pentaradio-2010-03-23.mp3", type="mp3").save()

short = "Im Studio begrüßen dürfen wir diesmal die wunderbare Zoe.Leela. Mit im Gepäck waren ihr DJ und Produzent DJ Skywax so wie Ihr Manager Tompigs."
long = "Themen der Sendung waren u.a. Zoe's durchstarten in der Musikwelt, die Freude am Musikvideo drehen und natürlich ihre aktuelle \"Queendom Come\"-Tour - die Zoe auch nach Dresden geführt hat - zur Erdbeerdisco. <br/> Ein Dank geht an Zoe.LeelA's Labelchef Marco Medkour von rec72.net"
e = Episode(name="Zoe.LeelA", category="pentamusic", link="0x003", author="koeart", date=datetime(2010,3,18), short=short, long=long)
e.save()
File(episode=e.id, info="Ogg Vorbis, 68.2 MB", name="pentaMusic0x003", link="http://ftp.c3d2.de/pentacast/pentamusic0x003.ogg", type="ogg").save()
File(episode=e.id, info="MPEG-Audio, 91.7 MB", name="pentaMusic0x003", link="http://ftp.c3d2.de/pentacast/pentamusic0x003.mp3", type="mp3").save()

short = "Was in den 1990er Jahren noch eine teure Zusatzerweiterung für den heimischen PC war, ist heute eine Selbstverständlichkeit: Sound."
long = "In diesem Podcast besprechen wir die Aufgaben und Funktionsweise einer Soundkarte, verschiedene Realisierungen von Soundsubsystemen in verschiedenen Betriebsystemen und gehen grundsätzlich auf Probleme aus dem Audiobereich im Zusammenhang mit dem Computer ein."
e = Episode(name="Echtzeit-Audio", category="pentacast", link="9", author="kl0bs", date=datetime(2010,3,3,22,23), short=short, long=long)
e.save()
File(episode=e.id, info="Ogg Vorbis, 62.6 MB", name="Pentacast 9: Echtzeit-Audio", link="http://ftp.c3d2.de/pentacast/pentacast-9-rtaudio.ogg", type="ogg").save()
File(episode=e.id, info="MPEG-Audio, 123.5 MB", name="Pentacast 9: Echtzeit-Audio", link="http://ftp.c3d2.de/pentacast/pentacast-9-rtaudio.mp3", type="mp3").save()


# run

run()

