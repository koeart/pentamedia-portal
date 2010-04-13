#!/usr/bin/env python3

## [c]3d2-[web]2[p]enta[m]edia[p]ortal konverter.. :)
# Was muss ich auswerten?
# > filename (regex: Anfang) ---> filename nach category=cast/music/radio + datum/Episode splitten
# > item.attrib (author, title, date) --> Episode(name="$title", category="$category", id="$date", author="$author", date=datetime(yy, mm, dd, hh, mm)))
# > Inhalt (<p>)bis <addendum> ---> "short description"
# > Inhalt bis </addendum> ---> "long description"
# > <resource></resource> ---> Download-link




from pprint import *
import xml.etree.ElementTree as etree
import xml.dom.minidom as dom

filename = "./pentamusic-0x001.xml"
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
print(short)

# long: alle Absätze ab <addendum> bis </addendum>

addendum = root.findall('addendum')
lang = etree.tostring(addendum[0])
print(lang)


