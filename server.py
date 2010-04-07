#!/usr/bin/env python3.0
from juno import init, redirect, route, run, get, \
                 model, \
                 subdirect, template, autotemplate
init({'static_url':'/s/*:file', '500_traceback':True, 'use_templates':True, 'bind_address':'',
  'use_db':True,
  'template_kwargs':{'extensions':["jinja2.ext.do","jinja2.ext.loopcontrols"]}})

#constants

head_colors = {'radio':"ffc8b4", 'cast':"b4c8ff", 'music':"c8ffc8"}

# models

File = model('File', episode='integer', name='string', filename='string', link='string')
Episode = model('Episode', name='string', link='string', category='string', author='string', date='datetime', short='text', long='text')
Comment = model('Comment', episode='integer', author='string', date='datetime', text='text')

# routes

autotemplate("/","start.html", css="start")


@route("/(?P<star>radio|cast|music)/:id")
def sendung(web,star,id):
  try:
    episode = Episode.find().filter_by(link=id).one()
  except: return redirect("/"+star)
  return template("sendung.tpl",header_color=head_colors[star],css="sendung",
                  episode=episode, site=star)


@route("/(?P<site>radio|cast|music)/")
def main(web,site):
  episodes = Episode.find().filter_by(category=site).order_by(Episode.date).limit(20).all()
  episodes.reverse()
  return template(site+".tpl",header_color=head_colors[site], css="sendung", \
                  episodepage=episodes)


# example content

from datetime import datetime # year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None

short = "Die Bundesrepublik - unendliche Bürokratie. Dies ist der Versuch des Pentacast etwas Licht ins Dunkel zu bringen."
long = "In dieser überaus spannenden und hitzigen Episode werden grundlegende Strukturen und Begriffe erklärt, die man für das Verständnis eines Rechtsstaates benötigt. Accuso, ein Volljurist aus dem Vereinsumfeld, steht Rede und Antwort und gibt ein paar aufschlussreiche Tips die dem Laien das Dickicht der Bürokratie und Juristerei algorithmisch zu durchdringen."
Episode(name="Rechtsstaat", category="cast", link="10", author="kl0bs", date=datetime(2010,4,4,16,14), short=short, long=long).save()

short = "Datenbanken sind die Leitz-Ordner der Rechenmaschinen. In ihnen wird versenkt, was man evtl. noch mal brauchen könnte. Daraus leiten sich zwei Probleme ab: Wie findet man diese Daten wieder und wie schnell kommt man wieder heran? Diese Probleme zu lösen haben relationale Datenbanksysteme über Jahrzehnte optimiert."
long = "Im Scope des Internets wird gleich ein 3. Problem offensichtlich: Wie viele Clients kommen quasi gleichzeitig an diese Daten ran? Wie schnell puhlt z. B. eine Suchmaschine die URL aus dem herunter geladenen Internet? <br/> Neue Lösungen sind also für die Datenhalden unserer Zeit gefragt. Wir reden mal etwas darüber, welche Ansätze es da so gibt, wie die Entwicklungen sind und geben Tipps, was Ihr auch mal in der eigenen Küche ausprobieren könnt. <br/> Ihr seid herzlich eingeladen anzurufen (0351/32 05 47 11) oder im c3d2 Channel mit uns zu chatten."
Episode(name="No, No, NoSQL, oder doch?", category="radio", link="032010", author="a8", date=datetime(2010,3,23,13,28), short=short, long=long).save()

short = "Im Studio begrüßen dürfen wir diesmal die wunderbare Zoe.Leela. Mit im Gepäck waren ihr DJ und Produzent DJ Skywax so wie Ihr Manager Tompigs."
long = "Themen der Sendung waren u.a. Zoe's durchstarten in der Musikwelt, die Freude am Musikvideo drehen und natürlich ihre aktuelle \"Queendom Come\"-Tour - die Zoe auch nach Dresden geführt hat - zur Erdbeerdisco. <br/> Ein Dank geht an Zoe.LeelA's Labelchef Marco Medkour von rec72.net"
Episode(name="Zoe.LeelA", category="music", link="0x003", author="koeart", date=datetime(2010,3,18), short=short, long=long).save()

short = "Was in den 1990er Jahren noch eine teure Zusatzerweiterung für den heimischen PC war, ist heute eine Selbstverständlichkeit: Sound."
long = "In diesem Podcast besprechen wir die Aufgaben und Funktionsweise einer Soundkarte, verschiedene Realisierungen von Soundsubsystemen in verschiedenen Betriebsystemen und gehen grundsätzlich auf Probleme aus dem Audiobereich im Zusammenhang mit dem Computer ein."
Episode(name="Echtzeit-Audio", category="cast", link="9", author="kl0bs", date=datetime(2010,3,3,22,23), short=short, long=long).save()


# run

run()

