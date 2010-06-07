
import json
from juno import route, redirect, template, header, append

from inc.db import File, Link, Episode, Comment
from inc.helper import build_comment_tree


@route("/comments[/.](?P<mode>(atom|json))")
def feed_all_comments(web, mode):
    # FIXME wrap db queries into one
    episodes = Episode.find().all()
    comments = Comment.find().all()
    comments.sort(key=lambda cmnt: cmnt.date)
    comments.reverse()
    if mode == "atom":
        id_episodes = {}
        for episode in episodes:
            id_episodes[episode.id] = episode
        return template_atom(
                        title    = "Pentamedia-Portal // Comments",
                        episodes = id_episodes,
                        comments = comments
                       )
    elif mode == "json":
        return template_json(web, list(map(comment_to_json, comments)))
    else:
        return redirect("/") # FIXME impl error


@route("/comments/count[/.]json")
def feed_all_comments_counts(web):
    episodes = Episode.find().all()
    comments = {}
    for episode in episodes:
        label = episode.filename.split("/").pop()
        comments[label] = len(Comment.find().filter_by(episode = episode.id).all())
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
    else:
        return redirect("/") # FIXME impl error


@route("/(?P<site>penta(radio|cast|music))/(?P<id>[^/]*)/comments[/.](?P<mode>(atom|json))")
def feed_comments_by_slug(web, site, id, mode):
    try: # FIXME wrap db queries into one
        episode  = Episode.find().filter_by(link = id).one()
        comments = Comment.find().filter_by(episode = episode.id).\
                    order_by(Comment.date).all()
    except: return template("comments.tpl", fail = True) # FIXME impl error
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
    except: return template("comments.tpl", fail = True) # FIXME impl error
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
    else:
        return redirect("/") # FIXME impl error


def comment_to_json(comment):
  return { "author": comment.author,
           "reply":  comment.reply,
           "date":   comment.fdate(),
           "text":   comment.text }


def template_atom(**kwargs):
    header('Content-Type', "application/atom+xml")
    return template("atom.tpl", **kwargs)


def template_json(web, data):
    value = json.dumps(data)
    if web.input('jsonp'):
        value = web.input('jsonp') + "(" + value + ");\n"
        header('Content-Type', "text/javascript")
    else:
        header('Content-Type', "application/json")
    response = append("")
    response.config['body'] = value
    return response




