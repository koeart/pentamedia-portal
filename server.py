#!/usr/bin/env python3.0
from time import time
from hashlib import sha1
from random import randint, random
from datetime import datetime # year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None
from juno import init, redirect, route, run, model, post, template, \
                 open_nutshell, close_nutshell, getHub, subdirect

# init

init({'static_url':      '/s/*:file',
      '500_traceback':   True,
      'use_templates':   True,
      'bind_address':    '',
      'use_db':          True,
      'use_sessions':    True,
      'template_kwargs':
         {'extensions':  ["jinja2.ext.do","jinja2.ext.loopcontrols"]}
     })

# import submitter

open_nutshell()
import submitter
submitter = getHub()
close_nutshell()

# constants

head_colors = {'radio': "ffc8b4",
               'cast':  "b4c8ff",
               'music': "c8ffc8"
              }
sections = {'radio': [("Pentasubmitter","/radio/submitter/")],
            'cast':  [],
            'music': []
           }

# cache

comment_hashes = {}

# models

File = model('File',
             episode = 'integer',
             info    = 'string',
             name    = 'string',
             link    = 'string'
            )
Episode = model('Episode',
                name     = 'string',
                link     = 'string',
                category = 'string',
                author   = 'string',
                date     = 'datetime',
                short    = 'text',
                long     = 'text'
               )
Comment = model('Comment',
                episode = 'integer',
                author  = 'string',
                date    = 'datetime',
                text    = 'text'
               )

# routes

@route("/")
def start(web): # FIXME wrap db queries into one
  episodes = dict([(c, reversed(Episode.find().\
                    filter_by(category=c).\
                    order_by(Episode.date).\
                    limit(13).all()))
                   for c in ['radio','music','cast'] ])
  return template("start.html",
                  episodes = episodes,
                  css      = "start"
                 )


@post("/(?P<site>radio|cast|music)/:id/comment/new")
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
    if now - comment_hashes[comment_try][0] > 600: # FIXME ten minutes !? puh .. thats very dirty ...
      del comment_hashes[comment_try]
  if found and \
     web.input('author')  is not None and \
     web.input('comment') is not None and \
     web.input('comment') != "":
    Comment(episode = episode.id,
            author  = web.input('author'),
            text    = web.input('comment'),
            date    = datetime.now()
           ).save()
  return redirect("/{0}/{1}".format(site,id))


@route(['radio/submitter', 'radio/submitter/:rest'])
def submitter_site(web, rest = ""):
  return subdirect(web, submitter, rest)


@route("/(?P<site>radio|cast|music)/:id")
def episode(web, site, id):
  try: # FIXME wrap db queries into one
    episode  = Episode.find().filter_by(link = id).one()
    files    = File.find().filter_by(episode = episode.id).all()
    comments = Comment.find().filter_by(episode = episode.id).\
                 order_by(Comment.date).all()
  except: return redirect("/{0}".format(site))
  a, b, c = randint(1, 10), randint(1, 10), randint(1, 10)
  hash = sha1(bytes(str(random()),'utf-8')).hexdigest()
  comment_hashes[hash] = (time(), a + b + c)
  return template("episode.tpl",
                  header_color = head_colors[site],
                  css          = "episode",
                  episode      = episode,
                  site         = site,
                  comments     = comments,
                  files        = files,
                  sections     = sections[site],
                  hash         = hash,
                  a = a, b = b, c = c
                 )


@route("/(?P<site>radio|cast|music)/")
def main(web, site):
  episodes = Episode.find().filter_by(category=site).\
               order_by(Episode.date).limit(20).all()
  episodes.reverse()
  # FIXME wrap db queries into one
  comments_count = [ Comment.find().filter_by(episode = e.id).count()
                     for e in episodes ]
  return template("episodes.tpl",
                  header_color= head_colors[site],
                  css         = "episode",
                  episodepage = zip(episodes, comments_count),
                  site        = site,
                  sections    = sections[site]
                 )


# example content

short = "Die Bundesrepublik - unendliche Bürokratie. Dies ist der Versuch des Pentacast etwas Licht ins Dunkel zu bringen."
long = "In dieser überaus spannenden und hitzigen Episode werden grundlegende Strukturen und Begriffe erklärt, die man für das Verständnis eines Rechtsstaates benötigt. Accuso, ein Volljurist aus dem Vereinsumfeld, steht Rede und Antwort und gibt ein paar aufschlussreiche Tips die dem Laien das Dickicht der Bürokratie und Juristerei algorithmisch zu durchdringen."
e = Episode(name="Rechtsstaat", category="cast", link="10", author="kl0bs", date=datetime(2010,4,4,16,14), short=short, long=long)
e.save()
File(episode=e.id, info="(Ogg Vorbis, 94.1 MB)", name="Pentacast 10: Rechtsstaat", link="http://ftp.c3d2.de/pentacast/pentacast-10-rechtsstaat.ogg").save()
File(episode=e.id, info="(MPEG-Audio, 190.8 MB)", name="Pentacast 10: Rechtsstaat", link="http://ftp.c3d2.de/pentacast/pentacast-10-rechtsstaat.mp3").save()

short = "Datenbanken sind die Leitz-Ordner der Rechenmaschinen. In ihnen wird versenkt, was man evtl. noch mal brauchen könnte. Daraus leiten sich zwei Probleme ab: Wie findet man diese Daten wieder und wie schnell kommt man wieder heran? Diese Probleme zu lösen haben relationale Datenbanksysteme über Jahrzehnte optimiert."
long = "Im Scope des Internets wird gleich ein 3. Problem offensichtlich: Wie viele Clients kommen quasi gleichzeitig an diese Daten ran? Wie schnell puhlt z. B. eine Suchmaschine die URL aus dem herunter geladenen Internet? <br/> Neue Lösungen sind also für die Datenhalden unserer Zeit gefragt. Wir reden mal etwas darüber, welche Ansätze es da so gibt, wie die Entwicklungen sind und geben Tipps, was Ihr auch mal in der eigenen Küche ausprobieren könnt. <br/> Ihr seid herzlich eingeladen anzurufen (0351/32 05 47 11) oder im c3d2 Channel mit uns zu chatten."
e = Episode(name="No, No, NoSQL, oder doch?", category="radio", link="032010", author="a8", date=datetime(2010,3,23,13,28), short=short, long=long)  
e.save()
File(episode=e.id, info="(Ogg Vorbis, 111.2 MB)", name="pentaradio24 vom 23. März 2010", link="http://ftp.c3d2.de/pentaradio/pentaradio-2010-03-23.ogg").save()
File(episode=e.id, info="(MPEG-Audio, 94.9 MB)", name="pentaradio24 vom 23. März 2010", link="http://ftp.c3d2.de/pentaradio/pentaradio-2010-03-23.mp3").save()

short = "Im Studio begrüßen dürfen wir diesmal die wunderbare Zoe.Leela. Mit im Gepäck waren ihr DJ und Produzent DJ Skywax so wie Ihr Manager Tompigs."
long = "Themen der Sendung waren u.a. Zoe's durchstarten in der Musikwelt, die Freude am Musikvideo drehen und natürlich ihre aktuelle \"Queendom Come\"-Tour - die Zoe auch nach Dresden geführt hat - zur Erdbeerdisco. <br/> Ein Dank geht an Zoe.LeelA's Labelchef Marco Medkour von rec72.net"
e = Episode(name="Zoe.LeelA", category="music", link="0x003", author="koeart", date=datetime(2010,3,18), short=short, long=long)
e.save()
File(episode=e.id, info="(Ogg Vorbis, 68.2 MB)", name="pentaMusic0x003", link="http://ftp.c3d2.de/pentacast/pentamusic0x003.ogg").save()
File(episode=e.id, info="(MPEG-Audio, 91.7 MB)", name="pentaMusic0x003", link="http://ftp.c3d2.de/pentacast/pentamusic0x003.mp3").save()

short = "Was in den 1990er Jahren noch eine teure Zusatzerweiterung für den heimischen PC war, ist heute eine Selbstverständlichkeit: Sound."
long = "In diesem Podcast besprechen wir die Aufgaben und Funktionsweise einer Soundkarte, verschiedene Realisierungen von Soundsubsystemen in verschiedenen Betriebsystemen und gehen grundsätzlich auf Probleme aus dem Audiobereich im Zusammenhang mit dem Computer ein."
e = Episode(name="Echtzeit-Audio", category="cast", link="9", author="kl0bs", date=datetime(2010,3,3,22,23), short=short, long=long)
e.save()
File(episode=e.id, info="(Ogg Vorbis, 62.6 MB)", name="Pentacast 9: Echtzeit-Audio", link="http://ftp.c3d2.de/pentacast/pentacast-9-rtaudio.ogg").save()
File(episode=e.id, info="(MPEG-Audio, 123.5 MB)", name="Pentacast 9: Echtzeit-Audio", link="http://ftp.c3d2.de/pentacast/pentacast-9-rtaudio.mp3").save()


# run

run()

