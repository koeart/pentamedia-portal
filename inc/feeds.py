
import json
from juno import route, redirect, template, header, append, notfound

from inc.db import File, Link, Episode, Comment, Trackback
from inc.helper import build_comment_tree


@route("/comments[/.](?P<mode>(atom|json))")
def feed_all_comments(web, mode):
    # FIXME wrap db queries into one
    episodes = Episode.find().all()
    comments = Comment.find().all()
    trackbacks = Trackback.find().all()
    if mode == "atom":
        entries = comments + trackbacks
        entries.sort(key=lambda e: e.date)
        entries.reverse()
        id_episodes = {}
        for episode in episodes:
            id_episodes[episode.id] = episode
        return template_atom(
                        title    = "Pentamedia-Portal // Comments",
                        episodes = id_episodes,
                        entries  = entries
                       )
    elif mode == "json":
        return template_json(web, {
            "comments":   list(map(comment_to_json, comments)),
            "trackbacks": list(map(trackback_to_json, trackbacks))
                           })
    else:  return notfound("Type not supported.")


@route("/comments/count[/.]json")
def feed_all_comments_counts(web):
    episodes = Episode.find().all()
    comments = {}
    for episode in episodes:
        label = episode.filename.split("/").pop()
        comments[label] = Comment.find().filter_by(episode = episode.id).count()
    return template_json(web, comments)


@route("/(?P<site>penta(radio|cast|music))/comments[/.](?P<mode>(atom|json))")
def feed_comments_by_category(web, site, mode):
    # FIXME wrap db queries into one
    episodes = Episode.find().filter_by(category = site).\
               order_by(Episode.date).all()
    episodes.reverse()
    comments, id_episodes = [], {}
    for episode in episodes:
        comments.extend(Comment.find().filter_by(episode = episode.id).all())
        id_episodes[episode.id] = episode
    comments.sort(key=lambda cmnt: cmnt.date)
    comments.reverse()
    if mode == "atom":
        return template_atom(
            title    = "Pentamedia-Portal // P{0} // Comments".format(site[1:]),
            episodes = id_episodes,
            comments = comments
                       )
    elif mode == "json":
        return template_json(web, {
            "comments": list(map(comment_to_json,comments)),
            "new_link": "/{0}/{1}/comment#new".format(episode.category,episode.link)
                                  })
    else: return  notfound("Type not supported.")


@route("/(?P<mode>(atom|json))")
def feed_episodes(web, mode):
    try:
        episodes = Episode.find().order_by(Episode.date).all()
    except: return notfound("No Episodes not found.")
    if mode == "atom":
        return template_episodes_atom(
            title = "Pentamedia-Portal // Episodes",
            episodes = episodes
                            )
    else: return notfound("Type not supported.")


@route("/(?P<site>penta(radio|cast|music))[/.](?P<mode>(atom|json))")
def feed_episodes_by_category(web, site, mode):
    try:
        episodes = Episode.find().filter_by(category = site).\
                    order_by(Episode.date).all()
    except: return notfound("Category not found.")
    if mode == "atom":
        return template_episodes_atom(
            title = "Pentamedia-Portal // P{0} // Episodes".format(site[1:]),
            episodes = episodes
                            )
    else: return notfound("Type not supported.")


@route("/(?P<site>penta(radio|cast|music))/(?P<id>[^/]*)/comments[/.](?P<mode>(atom|json))")
def feed_comments_by_slug(web, site, id, mode):
    try: # FIXME wrap db queries into one
        episode  = Episode.find().filter_by(link = id).one()
        comments = Comment.find().filter_by(episode = episode.id).\
                    order_by(Comment.date).all()
    except: return notfound("Episode not found.")
    return comments_per_episode(web, episode, comments, site, mode)


@route("/(?P<filename>(penta(radio24|cast|music))-.*)/comments[/.](?P<mode>(atom|json))")
def feed_comments_by_filename(web, filename, mode):
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
    return comments_per_episode(web, episode, comments, site, mode)

# helper

def comments_per_episode(web, episode, comments, site, mode):
    comments = build_comment_tree(comments)
    if mode == "atom":
        return template_atom(
            title    = "Pentamedia-Portal // {0} // Comments".format(episode.name),
            episodes = {episode.id: episode},
            comments = comments
                            )
    elif mode == "json":
        if web.input("html"):
            html = template("comments.inner_html.tpl",
                            isjson       = True,
                            episode      = episode,
                            site         = site,
                            comments     = comments
                           )
            return template_json(web, {
                "html"    : html.body,
                "new_link": "/{0}/{1}/comments/comment#new".format(site, episode.link)
                                })
        return template_json(web ,{
            "comments": list(map(comment_to_json,comments)),
            "new_link": "/{0}/{1}/comments/comment#new".format(episode.category, episode.link)
                            })
    else:  return notfound("Type not supported.")


def trackback_to_json(trackback):
    return { "title":     trackback.title,
             "excerpt":   trackback.text,
             "date":      trackback.fdate(),
             "url":       trackback.url,
             "blog_name": trackback.name }


def comment_to_json(comment):
  return { "author": comment.author,
           "reply":  comment.reply,
           "date":   comment.fdate(),
           "text":   comment.text }


def entry_to_json(entry):
    if isinstance(entry, Trackback): return trackback_to_json(entry)
    elif isinstance(entry, Comment): return comment_to_json(entry)


def template_episodes_atom(**kwargs):
    header('Content-Type', "application/atom+xml")
    return template("episodes_atom.tpl", **kwargs)


def template_atom(**kwargs):
    header('Content-Type', "application/atom+xml")
    return template("comments_atom.tpl", **kwargs)


def template_json(web, data):
    value = json.dumps(data)
    if web.input('jsonp'):
        value = web.input('jsonp') + "(" + value + ");\n"
        header('Content-Type', "text/javascript")
    else:
        header('Content-Type', "application/json")
    response = append("")
    response.config['body'] = ""
    return response.append(value)




