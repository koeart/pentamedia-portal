
from juno import route, get, post, yield_file, template, redirect, find, \
                 notfound, direct
from datetime import datetime # year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None
from sqlalchemy import and_
import os

from inc.re import re_reply, re_url
from inc.db import File, Link, Episode, Comment, Trackback, Rating, Preview
from inc.helper import cache, in_cache, clean_cache, create_session, \
                       do_the_comments, do_the_ratings
from inc.markdown import md
from inc.trackback import trackback_client
from config import pentamediaportal

# routes

import inc.feeds
import inc.trackback

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
            episode.append({'name': "more…", 'link': ""})
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
    except Exception as e: return notfound(str(e))
    yield_file("static/img/{0}acat{1}.jpeg".\
        format(not iscat and "not" or "", nr))


@route("/(?P<site>penta(radio|cast|music))/(?P<id>([^/](?!(atom|json)))*)(?P<mode>/(comment|rate|reply))?")
def episode(web, site, id, mode, errors=[]):
    try: # FIXME wrap db queries into one
        episode  = Episode.find().filter_by(link = id).one()
        files    = File.find().filter_by(episode = episode.id).all()
        links    = Link.find().filter_by(episode = episode.id).all()
        comments = Comment.find().filter_by(episode = episode.id).\
                   order_by(Comment.date).all()
        ratings  = Rating.find().filter_by(episode = episode.id).all()
        trackbacks = Trackback.find().filter_by(episode = episode.id).\
                     order_by(Trackback.date).all()
    except Exception as e: return notfound(str(e))
    if mode is None: mode = ""
    if len(mode): mode = mode[1:]
    opts = {}
    opts.update(create_session(web, mode))
    opts.update(do_the_comments(web, mode, comments))
    opts.update(do_the_ratings(web, mode, ratings))
    return template("episode.tpl",
                    errors     = errors,
                    css        = "episode",
                    episode    = episode,
                    episodes   = {episode.id: episode},
                    site       = site,
                    trackbacks = trackbacks,
                    files      = files,
                    links      = links,
                    csss       = [ "../lib/audio-js/audio-js",
                                   "../lib/audio-js/skins/vim",
                                   "vim"],
                    **opts
                   )


@route("/(?P<site>penta(radio|cast|music))(?!.*/(comment(s|/new)|rating(s)?))")
def main(web, site, errors=[]):
    try: # FIXME wrap db queries into one
        episodes = Episode.find().filter_by(category=site).\
                order_by(Episode.date).all()
        episodes.reverse()
        comments_count = [ Comment.find().filter_by(episode = e.id).count()
                        for e in episodes ]
        ratings = [ do_the_ratings(web, "", Rating.find().\
                    filter_by(episode = e.id).all())['rating']
                    for e in episodes ]
    except Exception as e: return notfound(str(e))
    return template("episodes.tpl",
                    errors      = errors,
                    css         = "episode",
                    episodepage = zip(episodes, comments_count, ratings),
                    site        = site
                   )


@route("/datenspuren/(?P<id>([^/](?!(atom|json)))+)(?P<mode>/(comment|rate|reply))?")
def datenspur(web, id, mode, errors=[]):
    try: # FIXME wrap db queries into one
        episodes = Episode.find().filter(Episode.category.endswith(id)).\
                order_by(Episode.date).all()
        episodes.reverse()
        comments_count = [ Comment.find().filter_by(episode = e.id).count()
                        for e in episodes ]
        ratings = [ do_the_ratings(web, "", Rating.find().\
                    filter_by(episode = e.id).all())['rating']
                    for e in episodes ]
        episode = Episode.find().filter_by(link = id).one()
        for ep in episodes:
            ep.has_screen = True
            ep.files = File.find().filter_by(episode = ep.id).all()
            ep.preview = get_preview(Preview.find().\
                filter_by(episode = episode.id).all(), ep.files)
        comments = Comment.find().filter_by(episode = episode.id).all()
        rating = Rating.find().filter_by(episode = episode.id).all()
    except Exception as e: return notfound(str(e))
    if mode is None: mode = ""
    if len(mode): mode = mode[1:]
    opts = {}
    opts.update(create_session(web, mode))
    opts.update(do_the_comments(web, mode, comments))
    opts.update(do_the_ratings(web, mode, rating))
    return template("datenspuren.tpl",
                    errors      = errors,
                    css         = "episode",
                    episodepage = zip(episodes, comments_count, ratings),
                    site        = "datenspuren",
                    full_site   = "datenspuren/" + id,
                    episode     = episode,
                    **opts
                   )


@route("/datenspuren/(?P<id>[^/]+)/(?P<filename>([^/](?!(atom|json)))+)(?P<mode>/(comment|rate|reply))?")
def datenspur_file(web, id, filename, mode, errors=[]):
    try: # FIXME wrap db queries into one
        episode = Episode.find().filter_by(link = filename).\
                filter(Episode.category.endswith(id)).\
                order_by(Episode.date).one()
        comments = Comment.find().filter_by(episode = episode.id).all()
        files    = File.find().filter_by(episode = episode.id).all()
        ratings  = Rating.find().filter_by(episode = episode.id).all()
        previews = Preview.find().filter_by(episode = episode.id).all()
        trackbacks = Trackback.find().filter_by(episode = episode.id).\
                    order_by(Trackback.date).all()
    except Exception as e: return notfound(str(e))
    episode.files = files
    if mode is None: mode = ""
    if len(mode): mode = mode[1:]
    opts = {}
    opts.update(create_session(web, mode))
    opts.update(do_the_comments(web, mode, comments))
    opts.update(do_the_ratings(web, mode, ratings))
    preview = get_preview(previews, files)
    csss = [ "../lib/video-js/video-js", "../lib/video-js/skins/vim", "vim"]
    if episode.isaudio():
        csss = list(map(lambda s:s.replace("video", "audio"), csss))
    return template("datenspur.tpl",
                    errors     = errors,
                    css        = "episode",
                    episode    = episode,
                    episodes   = {episode.id: episode},
                    site       = "datenspuren",
                    full_site  = "datenspuren/" + id,
                    trackbacks = trackbacks,
                    files      = files,
                    preview    = preview,
                    csss       = csss,
                    **opts
                   )


@route("/datenspuren(?!.*/(comment(s|/new)|rating(s)?))")
def datenspuren(web, errors=[]):
    try: # FIXME wrap db queries into one
        episodes = Episode.find().filter(Episode.category.startswith("ds")).\
                order_by(Episode.date).all()
        episodes.reverse()
        comments_count, ratings = [], []
        for episode in episodes:
            ids = list(map(lambda e:e.id, Episode.find(Episode.id).\
                filter_by(category = "file/{0}/{1}".\
                format(episode.category, episode.link)).all()))
            f_rts = Rating.find().filter(Rating.episode.in_(ids)).all()
            e_rts = Rating.find().filter_by(episode = episode.id).all()
            ratings += [ do_the_ratings(web, "", e_rts + f_rts)['rating'] ]
            comments_count += [
                Comment.find().filter(Comment.episode.in_(ids)).count() +
                Comment.find().filter_by( episode = episode.id).count() ]
            count = File.find().filter_by(episode = episode.id).count()
            episode.filescount = "// {0} File{1}".format(count,
                count != 1 and "s" or "")
    except Exception as e: return notfound(str(e))
    return template("episodes.tpl",
                    errors      = errors,
                    css         = "episode",
                    episodepage = zip(episodes, comments_count, ratings),
                    site        = "datenspuren"
                   )


@route("/(?P<site>penta(radio|cast|music))/(?P<id>[^/]*)/comments(?P<mode>[/.](comment|reply))?")
def comments(web, site, id, mode, errors=[]):
    try: # FIXME wrap db queries into one
        episode  = Episode.find().filter_by(link = id).one()
        comments = Comment.find().filter_by(episode = episode.id).\
                   order_by(Comment.date).all()
    except: return notfound("Episode not found.")
    return template_mode(web, site, episode, mode,
                         errors   = errors,
                         comments = comments
                        )


@route("/(?P<site>penta(radio|cast|music))/(?P<id>[^/]*)/rating(s)?(?P<mode>[/.]rate)?")
def ratings(web, site, id, mode, errors=[]):
    try: # FIXME wrap db queries into one
        episode  = Episode.find().filter_by(link = id).one()
        ratings = Rating.find().filter_by(episode = episode.id).all()
    except: return notfound("Episode not found.")
    return template_mode(web, site, episode,
                         (mode == '/' or mode is None) and "/rating" or mode,
                         errors             = errors,
                         hide_rating_detail = True,
                         ratings = ratings)


@route("/(?P<filename>(penta(radio24|cast|music))-.*)/comments(?P<mode>[/.](comment|reply))?")
def comments_by_filename(web, filename, mode, errors=[]):
    filename = "content/news/{0}.xml".format(filename)
    try: # FIXME wrap db queries into one
        episode  = Episode.find().filter_by(filename = filename).one()
        comments = Comment.find().filter_by(episode = episode.id).\
                   order_by(Comment.date).all()
        if   "radio" in filename: site = "pentaradio"
        elif "cast"  in filename: site = "pentacast"
        elif "music" in filename: site = "pentamusic"
        else: site = 42 / 0
    except Exception as e: return notfound(str(e))
    return template_mode(web, site, episode, mode,
                         errors   = errors,
                         comments = comments
                        )


@route("/(?P<filename>(penta(radio24|cast|music))-.*)/rating(s)?(?P<mode>[/.]rate)?")
def ratings_by_filename(web, filename, mode, errors=[]):
    filename = "content/news/{0}.xml".format(filename)
    try: # FIXME wrap db queries into one
        episode  = Episode.find().filter_by(filename = filename).one()
        ratings = Rating.find().filter_by(episode = episode.id).all()
        if   "radio" in filename: site = "pentaradio"
        elif "cast"  in filename: site = "pentacast"
        elif "music" in filename: site = "pentamusic"
        else: site = 42 / 0
    except Exception as e: return notfound(str(e))
    return template_mode(web, site, episode,
                         (mode == '/' or mode is None) and "/rating" or mode,
                         errors             = errors,
                         hide_rating_detail = True,
                         ratings = ratings)


@post("/(?P<site>penta(radio|cast|music))/:id/comment/new") # FIXME impl error
def new_comment(web, site, id):
    is_ok, result = get_episode_if_input_is_ok(web, Episode.link == id,
            exists   = ['author','comment','reply'],
            notempty = ['comment'] )
    if is_ok:
        build_and_save_comment(web, site+"/"+id, result)
        result = None
    else: return direct(web, "/{0}/{1}/comment".format(site,id),
            errors = [result or "Captcha wrong"])
    return result or redirect("/{0}/{1}".format(site,id))


@post("(?P<site>penta(radio|cast|music))/:id/rating/new")
def new_rating(web, site, id):
    is_ok, result = get_episode_if_input_is_ok(web, Episode.link == id,
            exists = ['score'], notempty = ['score'] )
    if is_ok:
        episode, result = result, None
        try:    score = int(web.input('score'))
        except: score = None
        if score is not None:
            if score in range(1,6):
                Rating(episode = episode.id, score = score).save()
    else: return direct(web, "/{0}/{1}/rate".format(site,id),
            errors = [result or "Captcha wrong"])
    return result or redirect("/{0}/{1}".format(site,id))


@post("/datenspuren/:id/:filename/comment/new") # FIXME impl error
def new_ds_file_comment(web, id, filename):
    is_ok, result = get_episode_if_input_is_ok(web,
            and_(Episode.link == filename, Episode.category.endswith(id)),
            exists   = ['author','comment','reply'],
            notempty = ['comment'] )
    if is_ok:
        build_and_save_comment(web, "datenspuren/{0}/{1}".format(id, filename), result)
        result = None
    else: return direct(web, "/datenspuren/{0}/comment".format(id),
            errors = [result or "Captcha wrong"])
    return result or redirect("/datenspuren/{0}/{1}".format(id, filename))


@post("datenspuren/:id/:filename/rating/new")
def new_ds_file_rating(web, id, filename):
    is_ok, result = get_episode_if_input_is_ok(web,
            and_(Episode.link == filename, Episode.category.endswith(id)),
            exists = ['score'], notempty = ['score'] )
    if is_ok:
        episode, result = result, None
        try:    score = int(web.input('score'))
        except: score = None
        if score is not None:
            if score in range(1,6):
                Rating(episode = episode.id, score = score).save()
    else: return direct(web, "/datenspuren/{0}/rate".format(id),
            errors = [result or "Captcha wrong"])
    return result or redirect("/datenspuren/{0}/{1}".format(id,filename))


@post("/datenspuren/:id/comment/new") # FIXME impl error
def new_ds_file_comment(web, id):
    is_ok, result = get_episode_if_input_is_ok(web, Episode.link == id,
            exists   = ['author','comment','reply'],
            notempty = ['comment'] )
    if is_ok:
        build_and_save_comment(web, "datenspuren/" + id, result)
        result = None
    else: return direct(web, "/datenspuren/{0}/comment".format(id),
            errors = [result or "Captcha wrong"])
    return result or redirect("/datenspuren/" + id)


@post("datenspuren/:id/rating/new")
def new_ds_file_rating(web, id):
    is_ok, result = get_episode_if_input_is_ok(web, Episode.link == id,
            exists = ['score'], notempty = ['score'] )
    if is_ok:
        episode, result = result, None
        try:    score = int(web.input('score'))
        except: score = None
        if score is not None:
            if score in range(1,6):
                Rating(episode = episode.id, score = score).save()
    else: return direct(web, "/datenspuren/{0}/rate".format(id),
            errors = [result or "Captcha wrong"])
    return result or redirect("/datenspuren/" + id)


@route("/spenden")
def donate(web):
    return template("spenden.tpl")


# helper


def captcha_is_ok(web):
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
    return found


def get_episode_if_input_is_ok(web, filtr, exists = [], notempty = []):
    if captcha_is_ok(web) and \
      all([ web.input(k) is not None for k in exists   ]) and \
      all([ web.input(k) != ""       for k in notempty ]):
        try:    return True, Episode.find().filter(filtr).one()
        except Exception as e: return False, str(e)
    return False, None


def build_and_save_comment(web, site, episode):
        text, reply = md.convert(web.input('comment')), []
        def replyer(x):
            a = x.group()[1:]
            i = find(Comment.id).filter_by(author=a).order_by(Comment.date).all()
            if i: reply.append(i[-1][0])
            return i and '@<a href="/{0}/reply?{1}#new">{2}</a>'.\
                         format(site, i[-1][0], a)\
                     or "@{0}".format(a)
        text = re_reply.sub(replyer, text)
        if reply: reply = reply[0]
        else:     reply = -1
        if web.input('reply') != "-1":
            try: reply = int(web.input('reply'))
            except: pass
        cat = episode.category
        if "ds" in cat: cat = "datenspuren"
        pm_url = pentamediaportal + "/{0}/{1}".format(cat, episode.link)
        for link in re_url.finditer(web.input('comment')):
            trackback_client(link.group(), pm_url,
                             title   = episode.name,
                             excerpt = web.input('comment')
                            )
        Comment(episode = episode.id,
                author  = web.input('author'),
                reply   = reply,
                text    = text,
                date    = datetime.now()
               ).save()
        notify_muc("{0} just left some pithy words on {1}. [ {2} ]".\
            format(web.input('author'), episode.name, pm_url))


def get_preview(previews, files):
    previews = dict([ (preview.link, preview) for preview in previews ])
    preview = None
    for f in files:
        if f.link in previews:
            preview = previews[f.link]
            break
    return preview


def template_comments():
    return "comments.tpl", do_the_comments


def template_rating():
    return "rating.tpl", do_the_ratings


_template_functions = {
        "reply"   : template_comments,
        "comment" : template_comments,
        "rate"    : template_rating,
        "rating"  : template_rating,
    }


def template_mode(web, site, episode, mode, **kwargs):
    opts, func = {}, template_comments
    if mode is None: mode = ""
    if len(mode): mode = mode[1:]
    if mode in _template_functions:
        func = _template_functions[mode]
    tpl, worker = func()
    kwargs = dict(kwargs)
    kwargs.update(site = site, episode = episode)
    wopts = worker(web, mode, **kwargs)
    opts.update(create_session(web, mode))
    opts.update(css = "episode")
    opts.update(kwargs)
    opts.update(wopts)
    return template(tpl, **opts)


def notify_muc(text):
    cmd = 'curl --data-urlencode "text={0}" http://www.hq.c3d2.de/bot/msg'.format(text)
    os.system(str(cmd.encode('ascii', 'replace'), 'utf-8'))
