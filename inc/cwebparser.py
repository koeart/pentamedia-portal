#!/usr/bin/env python3

## [c]3d2-[web]2[p]enta[m]edia[p]ortal konverter.. :)

import re
from datetime import datetime
import xml.etree.ElementTree as etree

re_filename = re.compile(r".*(?P<type>penta(cast|radio|music)).*-(?P<episode>\w*)\.xml")


# FIXME add more types (if needed)
FILETYPE = {'x-bittorrent': "BitTorrent-Metainformationen",
            'x-zip': "Zip-Archiv",
            'ogg': "Ogg Vorbis Audio",
            'mpeg': "MPEG-Audio",
            'mp3': "MPEG-Audio"
           }

FILESIZE = ["KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"] # ready for da future :P
FILEBLOCK = 1024


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
    raw = "".join([ etree.tostring(n).\
                replace("<link", "<a").replace("</link>", "</a>")
                + "\n" for n in p[1:] ])
    lang = raw.strip()[3:-4].strip()
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
    return link.attrib['href'] if 'href' in link.attrib else link.text

def get_link(litag):
    return {'title': get_title(litag),
            'url': get_url(litag)
           }

def get_links(root):
    addendum = root.findall('addendum')
    try: addendum = addendum[0]
    except: return []
    ultags = addendum.findall('ul')
    litags = sum([ [ li for li in ul.findall('li') if li.findall('link') ]
                for ul in ultags ],[])
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
    ogg = get_ogg(resource)
    alternative = resource.findall('alternative')
    try: alternative = alternative[0]
    except: return [ogg]
    mp3 = get_mp3(alternative, ogg['name'])
    return [ogg, mp3]


def get_files(root):
    resources = root.findall('resource')
    return sum(map(get_audio,resources), [])



def load_podcast_file(filename):
    tree = etree.parse(filename)
    root = tree.getroot()
    return {'episode': get_episode(filename, root),
            'links': get_links(root),
            'files': get_files(root)
           }


def test():
    from pprint import pprint
    filename = "./pentamusic-0x001.xml"
    #filebase = "../c3d2-web/content/news/" #wo liegen dateien? RELATIV!!!
    #with open("pentafiles.txt", "r") as text:
            #for line in text:
                  #raw = filebase + line
                  #filename = raw.rstrip()
    pprint(load_podcast_file(filename))

if __name__ == "__main__":
    test()


