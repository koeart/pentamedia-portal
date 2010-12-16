#!/usr/bin/env python3

## [c]3d2-[web]2[p]enta[m]edia[p]ortal konverter.. :)

import re
from datetime import datetime
import xml.etree.ElementTree as etree

re_podcast = re.compile(r".*(?P<type>penta(cast|radio|music))(-?\d*)-(?P<episode>[^.]*)\.xml")
re_recording = re.compile(r".*(?P<episode>(?P<type>d(s|atenspuren20)[^-]*)-[^.]*)\.xml")

# FIXME add more types (if needed)
FILETYPE = {'application/x-bittorrent': "BitTorrent-Metainformationen",
            'application/pdf': "Portable Document Format",
            'multipart/x-zip': "Zip-Archiv",
            'video/mp4': "MP4-Video",
            'video/webm': "WebM Video",
            'video/x-flv': "Flash Video",
            'video/ogg': "Ogg Media Video",
            'audio/ogg': "Ogg Vorbis Audio",
            'application/ogg': "Ogg Vorbis Audio",
            'audio/mpeg': "MPEG-Audio",
            'audio/mp3': "MPEG-Audio"
           }

FILESIZE = ["KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"] # ready for da future :P
FILEBLOCK = 1024


# parsers


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


def parse_link_tags(raw):
    return raw.replace("<link", "<a").replace("</link>", "</a>")


# workers


def get_name(tag):
    return tag.attrib['title']


def get_slug(rex, filename):
    m = rex.match(filename)
    episode = str(m.group('episode'))
    return episode


def get_category_by_rex(rex, filename):
    m = rex.match(filename)
    typ = str(m.group('type'))
    return typ


def get_save_category_by_rex(rex, filename):
    m = rex.match(filename)
    return str(m.group('type')) if m else None

def get_author(root):
    return root.attrib['author']


def get_date(root):
    raw = root.attrib['date']
    return parse_date(raw)


def get_short(root):
    p = root.findall('p')
    raw = etree.tostring(p[0]).strip()[3:-4].strip()
    return parse_link_tags(raw)


def get_long(root):
    p = root.findall('p')
    raw = "".join([ parse_link_tags(etree.tostring(n)) + "\n" for n in p[1:] ])
    lang = raw.strip()[3:-4].strip()
    return lang


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


def get_full_filetype(tag):
    return tag.attrib['type']


def get_filetype(tag):
    return get_full_filetype(tag).partition("/")[2]


def get_info(tag):
    size = parse_size(tag.attrib['size'])
    typ = FILETYPE[get_full_filetype(tag)]
    return "{0}, {1}".format(typ, size)


def get_filelink(tag):
    return tag.attrib['url']


def get_media(resource):
    res = get_resource(resource)
    alternatives = resource.findall('alternative')
    res['alternatives'] = list(map(lambda a:get_alternative(a,res['name']),
        alternatives))
    return res


def get_files(root):
    resources = root.findall('resource')
    return list(map(get_media,resources))


# helpers


def get_podcast_category(filename):
    return get_category_by_rex(re_podcast, filename)


def get_recording_category(filename):
    return get_category_by_rex(re_recording, filename).replace("atenspuren20", "s")


def get_save_podcast_category(filename):
    return get_save_category_by_rex(re_podcast, filename)


def get_save_recording_category(filename):
    cat = get_save_category_by_rex(re_recording, filename)
    if cat is not None: cat = cat.replace("atenspuren20", "s")
    return cat


def get_podcast_slug(filename):
    return get_slug(re_podcast, filename)


def get_recording_slug(filename):
    return get_slug(re_recording, filename)


# packers


def get_episode(filename, root):
    return {'name': get_name(root),
            'link': get_podcast_slug(filename),
            'category': get_podcast_category(filename),
            'author': get_author(root),
            'date': get_date(root),
            'short': get_short(root),
            'long': get_long(root)
           }


def get_recording(filename, root):
    return {'name': get_name(root),
            'link': get_recording_slug(filename),
            'category': get_recording_category(filename),
            'author': get_author(root),
            'date': get_date(root),
            'short': get_short(root),
            'long': get_long(root)
           }


def get_resource(tag):
    return {'name': get_name(tag),
            'type': get_filetype(tag),
            'link': get_filelink(tag),
            'info': get_info(tag)
           }


def get_alternative(tag, title):
    return {'name': title,
            'type': get_filetype(tag),
            'link': get_filelink(tag),
            'info': get_info(tag)
           }


# exports


def flatten_files(files):
    return sum(map(lambda f: sum(
        reversed([f.pop('alternatives'), [f]]), []), files), [])


def get_category(fn):
    return get_save_podcast_category(fn) or get_save_recording_category(fn)


def load_podcast_file(filename):
    tree = etree.parse(filename)
    root = tree.getroot()
    return {'episode': get_episode(filename, root),
            'links': get_links(root),
            'files': flatten_files(get_files(root)),
            'type': "podcast"
           }


def load_recording_file(filename):
    tree = etree.parse(filename)
    root = tree.getroot()
    return {'episode': get_recording(filename, root),
            'files': get_files(root),
            'type': "recording"
           }


def test():
    from pprint import pprint
    #filename = "./pentamusic-0x001.xml"
    #filebase = "../c3d2-web/content/news/" #wo liegen dateien? RELATIV!!!
    #with open("pentafiles.txt", "r") as text:
            #for line in text:
                  #raw = filebase + line
                  #filename = raw.rstrip()
    #pprint(load_podcast_file(filename))

    #filename = "./ds10-videomitschnitte-online.xml"
    filename = "./datenspuren2005-audio.xml"
    pprint(load_recording_file(filename))


if __name__ == "__main__":
    test()


