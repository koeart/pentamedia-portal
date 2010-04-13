#!/usr/bin/env python3

## [c]3d2-[web]2[p]enta[m]edia[p]ortal konverter.. :)
# Was muss ich auswerten?
# > filename (regex: Anfang) ---> filename nach category=cast/music/radio + datum/Episode splitten
# > item.attrib (author, title, date) --> Episode(name="$title", category="$category", id="$date", author="$author", date=datetime(yy, mm, dd, hh, mm)))
# > Inhalt (<p>)bis <addendum> ---> "short description"
# > Inhalt bis </addendum> ---> "long description"
# > <resource></resource> ---> Download-link




from pprint import *
import re
import xml.etree.ElementTree as etree

filename = "./pentamusic-0x001.xml"
c = re.compile(r"\.\/penta(?P<type>\w*)-(?P<episode>\w*)")
m = c.match(filename)
typ = str(m.groupdict('type'))
episode = str(m.groupdict('episode'))
print("Type: " + typ + ", Episode: " + episode)
print(typ)
tree = etree.parse(filename)
root = tree.getroot()


author = root.attrib['author']
title = root.attrib['title']
date = root.attrib['date']
print("Autor: {0}, Titel: {1}, Datum: {2}".format(author, title, date))

# short: Alle Absätze (<p></p>) bis <addendum>
p = root.findall('p')
short = ""
for n in p:
    short += etree.tostring(n)

# long: alle Absätze ab <addendum> bis </addendum>

addendum = root.findall('addendum')
lang = etree.tostring(addendum[0])

resource = root.findall('resource')
l_ogg = resource[0].attrib
ogg_url = l_ogg['url']
ogg_size = int(l_ogg['size'])
ogg_type = l_ogg['type']
ogg_title = l_ogg['title']
alternative = resource[0].findall('alternative')
l_mp3 = alternative[0].attrib
mp3_url = l_mp3['url']
mp3_size = int(l_mp3['size'])
mp3_type = l_mp3['type']





