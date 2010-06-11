
from urllib.request import urlopen
from urllib.parse import urlencode, urljoin
from datetime import datetime
from juno import post, template, header

from inc.re import re_trackback, re_url
from inc.db import Episode, Trackback
from inc.markdown import md


@post("/trackback/(?P<id>([0-9]*))")
def trackback_server(web, id):
    try: episode = Episode.find().filter_by(id = int(id)).one()
    except: return errör("Episode not found.")
    if not web.input('url'):
        return errör("No URL given.")
    spam = is_spam(web.input('url'), episode)
    if spam == 2:
        return errör("Timeout.")
    elif spam:
        return errör("Spam.")
    if web.input("excerpt"): text = md.convert(web.input('excerpt'))
    else: text = None
    Trackback(episode = episode.id,
              title   = web.input('title'),
              text    = text,
              url     = web.input('url'),
              date    = datetime.now(),
              name    = web.input('blog_name')
             ).save()
    return template_tb()


def trackback_client(link, url, title = None, excerpt = None):
    lrel = None
    for m in re_trackback.finditer(fetch_site(link)):
        if m:
            lrel = m.group('rela') or m.group('relb')
            if lrel and lrel.lower() == "trackback": break
    if not lrel or lrel.lower() != "trackback": return False
    lurl = m.group('urla') or m.group('urlb')
    if not lurl: return False
    if not re_url.match(lurl): lurl = urljoin(link, lurl)
    kwargs = {"blog_name": "C3D2 Pentamedia Portal",
              "url":       url }
    if excerpt: kwargs['excerpt'] = excerpt
    if title: kwargs['title'] = title
    print(link, lurl)
    return send_post(lurl, **kwargs)

# helper

def errör(msg):
    return template_tb(code = 1, message = msg)


def template_tb(**kwargs):
    response = template("trackback.tpl",**kwargs)
    header('Content-Type',"text/xml")
    return response


def fetch_site(url):
    try: f = urlopen(url,timeout = 3)
    except: f = None
    if f and "html" in f.info().get_content_type().lower():
        try: text = f.read()
        except: return ""
        try:    return str(text,'utf-8')
        except: return str(text)
    else:       return ""


def send_post(link, **data):
    try: f = urlopen(link,urlencode(data),timeout = 3)
    except: f = None
    if f:
        try: text = f.read()
        except: return ""
        try:    return str(text,'utf-8')
        except: return text
    else:       return False


def is_spam(url, episode):
    if not re_url.match(url): return True
    site = fetch_site(url)
    if site == "": return 2
    slug = "/{0}/{1}".format(episode.category,episode.link)
    label = episode.filename.split("/").pop()
    return slug not in site and label not in site # FIXME this check is really crap :P
