
from juno import route, get, post, yield_file, template, redirect, find, \
                 notfound
from datetime import datetime # year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None

from inc.re import re_reply
from inc.db import File, Link, Episode, Comment
from inc.helper import cache, in_cache, clean_cache, do_the_comments
from inc.markdown import md

# routes

import inc.feeds

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


@get("/cat/(?P<typ>[A-Z])")
def cat_image(web, typ):
    try:
        hash = web['QUERY_STRING']
        iscat = typ in cache(hash)[2]
        nr = cache(hash)[3][ord(typ)-65]
    except: return notfound("File not Found.")
    yield_file("static/img/{0}acat{1}.jpeg".\
        format(not iscat and "not" or "", nr))


@route("/(?P<site>penta(radio|cast|music))/(?P<id>([^/](?!(atom|json)))*)(?P<cmnt>/(comment|reply))?")
def episode(web, site, id, cmnt):
    try: # FIXME wrap db queries into one
        episode  = Episode.find().filter_by(link = id).one()
        files    = File.find().filter_by(episode = episode.id).all()
        links    = Link.find().filter_by(episode = episode.id).all()
        comments = Comment.find().filter_by(episode = episode.id).\
                   order_by(Comment.date).all()
    except: return notfound("Episode not found.")
    if cmnt is None: cmnt = ""
    if len(cmnt): cmnt = cmnt[1:]
    comments, reply, author, hash, a, b, c = do_the_comments(web, comments, cmnt)
    return template("episode.tpl",
                    comment_form = cmnt != "",
                    css          = "episode",
                    episode      = episode,
                    episodes     = {episode.id: episode},
                    site         = site,
                    comments     = comments,
                    files        = files,
                    links        = links,
                    reply        = reply,
                    at_author    = author,
                    hash         = hash,
                    a = a, b = b, c = c
                   )


@route("/(?P<site>penta(radio|cast|music))(?!.*/comments)")
def main(web, site):
    # FIXME wrap db queries into one
    episodes = Episode.find().filter_by(category=site).\
               order_by(Episode.date).all()
    episodes.reverse()
    comments_count = [ Comment.find().filter_by(episode = e.id).count()
                       for e in episodes ]
    return template("episodes.tpl",
                    css         = "episode",
                    episodepage = zip(episodes, comments_count),
                    site        = site
                   )


@route("/(?P<site>penta(radio|cast|music))/(?P<id>[^/]*)/comments(?P<mode>[/.](comment|reply))?")
def comments(web, site, id, mode):
    try: # FIXME wrap db queries into one
        episode  = Episode.find().filter_by(link = id).one()
        comments = Comment.find().filter_by(episode = episode.id).\
                   order_by(Comment.date).all()
    except: return notfound("Episode not found.")
    return template_comments(web, site, episode, comments, mode)


@route("/(?P<filename>(penta(radio24|cast|music))-.*)/comments(?P<mode>[/.](comment|reply))?")
def comments_by_filename(web, filename, mode):
    filename = "content/news/{0}.xml".format(filename)
    try: # FIXME wrap db queries into one
        episode  = Episode.find().filter_by(filename = filename).one()
        comments = Comment.find().filter_by(episode = episode.id).\
                   order_by(Comment.date).all()
        if   "radio" in filename: site = "pentaradio"
        elif "cast"  in filename: site = "pentacast"
        elif "music" in filename: site = "pentamusic"
        else: site = 42 / 0
    except: return notfound("Episode not found.")
    return template_comments(web, site, episode, comments, mode)


@post("/(?P<site>penta(radio|cast|music))/:id/comment/new") # FIXME impl error
def new_comment(web, site, id, isjson):
    try:    episode = Episode.find().filter_by(link = id).one()
    except: return redirect("/{0}".format(site)) # FIXME impl error
    found, hash = False, web.input('hash')
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
        if in_cache(hash):
            found = cache(hash)[typ] == tip
    clean_cache(hash)
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
    return redirect("/{0}/{1}".format(site,id)) # FIXME maybe error

# helper

def template_comments(web, site, episode, comments, cmnt):
    if cmnt is None: cmnt = ""
    if len(cmnt): cmnt = cmnt[1:]
    comments, reply, author, hash, a, b, c = do_the_comments(web, comments, cmnt)
    return template("comments.tpl",
                    comment_form = cmnt != "",
                    css          = "episode",
                    episode      = episode,
                    site         = site,
                    comments     = comments,
                    reply        = reply,
                    at_author    = author,
                    hash         = hash,
                    a = a, b = b, c = c
                   )

