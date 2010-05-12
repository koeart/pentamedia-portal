#!/usr/bin/env python3

## [c]3d2-[web]2[p]enta[m]edia[p]ortal konverter.. :)
# Was muss ich auswerten?
# > filename (regex: Anfang) ---> filename nach category=cast/music/radio + datum/Episode splitten
# > item.attrib (author, title, date) --> Episode(name="$title", category="$category", id="$date", author="$author", date=datetime(yy, mm, dd, hh, mm)))
# > Inhalt (<p>)bis <addendum> ---> "short description"
# > Inhalt bis </addendum> ---> "long description"
# > <resource></resource> ---> Download-link
# links = list(p); text = re.sub(r"(<(?!/)[^>]+>(.(?!</))*.</[^>]+>)",lambda x: "".join([ '<a{0}>{1}</a>'.format("".join([ ' {0}="{1}"'.format(*i) for i in _.attrib.items() ]),_.text) for _ in [links.pop(0)] ]),etree.tostring(p).strip()[2+len(p.tag):-3-len(p.tag)].strip()); print(text)




from datetime import datetime
import re
import xml.etree.ElementTree as etree

re_filename = re.compile(r"\.\/penta(?P<type>\w*).*-(?P<episode>\w*)\.xml")


# FIXME add more types (if needed)
FILETYPE = {'ogg': "Ogg Vorbis",
            'mpeg': "MPEG-Audio",
            'mp3': "MPEG-Audio"
           }
FILESIZE = ["KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"] # ready for da future :P
FILEBLOCK = 1024
#m = c.match(filename)
#typ = str(m.groupdict('type'))
#episode = str(m.groupdict('episode'))
#print("Type: " + typ + ", Episode: " + episode)
#print(typ)


def get_name(tag):
    return tag.attrib['title']

def parse_date(date):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

def parse_size(size):
    size = float(size)
    if size < FILEBLOCK:
        return "{0} B".format(size)
    for suffix in FILESIZE:
        size /= FILEBLOCK
        if size < FILEBLOCK:
            return "{0:.1f} {1}".format(size, suffix)
    return "{0:.1f} {1}".format(size, FILESIZE[-1]) # futurity NOW :)



def get_slug(filename):
    m = re_filename.match(filename)
    episode = str(m.group('episode'))
    return episode

def get_category(filename):
    m = re_filename.match(filename)
    typ = str(m.group('type'))
    return typ

def get_author(root):
    return root.attrib['author']

def get_date(root):
    raw = root.attrib['date']
    return parse_date(raw)

def get_short(root):
    p = root.findall('p')
    raw = etree.tostring(p[0]).strip()[3:-4].strip()
    short = raw.replace("<link", "<a").replace("</link>", "</a>")
    return short

def get_long(root):
    p = root.findall('p')
    lang = "".join([ etree.tostring(n).strip()[3:-4].strip().\
                replace("<link", "<a").replace("</link>", "</a>")
                + "\n" for n in p ])
    # FIXME addendum Absätze?!!!!
    return lang

def get_episode(filename, root):
    return {'name': get_name(root),
            'link': get_slug(filename),
            'category': get_category(filename),
            'author': get_author(root),
            'date': get_date(root),
            'short': get_short(root),
            'long': get_long(root)
           }


def get_title(litag):
    link = litag.findall('link')[0]
    return link.text

def get_url(litag):
    link = litag.findall('link')[0]
    return link.attrib['href']

def get_link(litag):
    return {'title': get_title(litag),
            'url': get_url(litag)
           }

def get_links(root):
    addendum = root.findall('addendum')[0]
    ultags = addendum.findall('ul')
    litags = sum([ ul.findall('li') for ul in ultags ],[])
    return list(map(get_link,litags))


def get_filetype(tag):
    return tag.attrib['type'].partition("/")[2]

def get_info(tag):
    size = parse_size(tag.attrib['size'])
    typ = FILETYPE[get_filetype(tag)]
    return "{0}, {1}".format(typ, size)

def get_filelink(tag):
    return tag.attrib['url']

def get_ogg(tag):
    return {'name': get_name(tag),
            'type': get_filetype(tag),
            'link': get_filelink(tag),
            'info': get_info(tag)
           }

def get_mp3(tag, title):
    return {'name': title,
            'type': get_filetype(tag),
            'link': get_filelink(tag),
            'info': get_info(tag)
           }

def get_audio(resource):
    alternative = resource.findall('alternative')[0]
    ogg = get_ogg(resource)
    mp3 = get_mp3(alternative, ogg['name'])
    return [ogg, mp3]

    
def get_files(root):
    resources = root.findall('resource')
    return sum(map(get_audio,resources), [])

#resource = root.findall('resource')
#l_ogg = resource[0].attrib
#ogg_url = l_ogg['url']
#ogg_size = int(l_ogg['size'])
#ogg_type = l_ogg['type']
#ogg_title = l_ogg['title']
#alternative = resource[0].findall('alternative')
#l_mp3 = alternative[0].attrib
#mp3_url = l_mp3['url']
#mp3_size = int(l_mp3['size'])
#mp3_type = l_mp3['type']



def load_file(filename):
    tree = etree.parse(filename)
    root = tree.getroot()
    return {'episode': get_episode(filename, root),
            'links': get_links(root),
            'files': get_files(root)
           }


#author = root.attrib['author']
#title = root.attrib['title']
#date = root.attrib['date']
#print("Autor: {0}, Titel: {1}, Datum: {2}".format(author, title, date))

# short: Alle Absätze (<p></p>) bis <addendum>
#p = root.findall('p')
#links = list(p); text = re.sub(r"(<(?!/)[^>]+>(.(?!</))*.</[^>]+>)",lambda x: "".join([ '<a{0}>{1}</a>'.format("".join([ ' {0}="{1}"'.format(*i) for i in _.attrib.items() ]),_.text) for _ in [links.pop(0)] ]),etree.tostring(p).strip()[2+len(p.tag):-3-len(p.tag)].strip()); print(text)
#for n in p:
#short = "" + etree.tostring(p[0]).strip()[3:-4].strip().replace("<link", "<a").replace("</link>", "</a>")
#print(short + "\n")

# long: alle Absätze ab <addendum> bis </addendum>


#lang =""
#for n in p:
#    lang += etree.tostring(n).strip()[3:-4].strip().replace("<link", "<a").replace("</link>", "</a>") + "\n"

#addendum = root.findall('addendum')
#p = addendum[0].findall('p')
#for n in p:
#    lang += etree.tostring(n).strip()[3:-4].strip().replace("<link", "<a").replace("</link>", "</a>") + "\n"

#print(lang)




#pprint(resource[0].attrib)
# Wie solls weitergehn?
#setup funktion basteln, die dict[] haben will
#def setup(dict):
#    asdf
#    adsf
#    asfd
#    af

#def import_xml(filename)
#    werte = 
#    wert2
#    wert4
#    dict['Episode']('wert1' 'wert2')

def test():
    from pprint import pprint
    filename = "./pentamusic-0x001.xml"
    pprint(load_file(filename))

if __name__ == "__main__":
    test()


