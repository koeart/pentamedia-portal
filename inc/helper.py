
import json
from math import floor
from time import time as now
from hashlib import sha1
from random import randint, random, shuffle
from juno import find

from inc.db import Comment

# cache

comment_hashes = {}

def cache(hash):
    return comment_hashes[hash]

def in_cache(hash):
    return hash in comment_hashes

def clean_cache(hash=None):
    if hash is not None:
        if hash in comment_hashes:
            del comment_hashes[hash]
    for comment_try in list(comment_hashes.keys()):
        if now() - comment_hashes[comment_try][0] > 10400: # 12 hours
            del comment_hashes[comment_try]

# helper


def build_comment_tree(comments):
    replying, idcomments = {}, {}
    for comment in list(comments):
      comment.level, idcomments[comment.id] = 0, comment
      r = comment.reply
      if r != -1:
          comments.remove(comment)
          if not r in replying:
              replying[r] = []
          replying[r].append(comment)
    level_replying = sum(replying.values(),[])
    while replying: # ups .. what a crapy code
      stash = []
      for comment in comments:
          stash.append(comment)
          if comment.id in replying:
              stash += replying[comment.id]
              del replying[comment.id]
      comments = stash
    for reply in level_replying:
        cur = reply
        while cur.reply != -1:
            reply.level += 1
            cur = idcomments[cur.reply]
    return comments


def _create_session(web, mode):
    try:
        reply = int(web['QUERY_STRING'])
        author = find(Comment.author).filter_by(id = reply).one()[0]
        author = "@{0} ".format(author)
    except: reply, author = -1, ""
    a, b, c = randint(1, 10), randint(1, 10), randint(1, 10)
    hash = sha1(bytes(str(random()),'utf-8')).hexdigest()
    if mode in ["comment", "rate", "reply"]:
        cats = [ chr(65+i) for i in range(4) if randint(0, 1) ]
        if not len(cats): cats = [chr(65+randint(0, 3))]
        elif len(cats) == 4: cats.pop(randint(0, 3))
        pics = list(range(16)); shuffle(pics); pics = pics[:4]
        comment_hashes[hash] = (now(), a + b + c, cats, pics)
    return reply, author, hash, a, b, c


def create_session(web, mode):
    reply, author, hash, a, b, c = _create_session(web, mode)
    return {'reply'     : reply,
            'at_author' : author,
            'hash'      : hash,
            'a' : a, 'b' : b, 'c' : c }


def do_the_comments(_, mode, comments = [], **kwargs):
    comments = build_comment_tree(comments)
    return {'comments' : comments , 'comment_form' : mode not in ["", "rate"] }


def do_the_ratings(_, mode, ratings = [], **kwargs):
    score = 0
    for r in ratings:
        score += r.score
    if ratings:
        score /= len(ratings)
    score = floor(score)
    return {'rating'      : { 'score' : score,
                              'count' : len(ratings),
                              'stars' : "★" * score + "☆" * (5 - score) },
            'rating_form' : mode == "rate",
            'enumerate'   : enumerate }

