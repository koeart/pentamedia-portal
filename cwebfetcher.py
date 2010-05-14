#!/usr/bin/env python3

# CONFIG

update_all = False
debug      = False
# ------

import re
import os
import os.path as ospath
from subprocess import getoutput, getstatusoutput
from cweb2pmp import load_file
from juno import init, session

init({'use_db':          True,
      'db_location':     "db.sqlite"
     })

from db import *


re_news = re.compile(r"(?P<file>content/news/penta(cast|music|radio).*\.xml)")
git = "git --git-dir=cweb.git --work-tree=. "

def main():
    log = ""

    git_test = getoutput("git log --format=%n")
    if "fatal" in git_test or "--format" in git_test:
        print("ERROR: your git version is to old.")
        os.system("git --version")
        exit(1)

    if not os.path.exists("cweb.git"):
        print("* no c3d2-web git repository found")
        os.mkdir("cweb.git")
        os.system(git+"init")
        os.system(git+"remote add web git://194.77.75.60/c3d2-web/git.git")
        if os.system(git+"fetch web master") == 0:
            print("* get filenames from log")
            log = getoutput(git+"log --name-only --format=%n FETCH_HEAD")
        else:
            print("* an error occured during fetch")
            exit(1)
    else:
        print("* fetching updates")
        fulllog, old = getstatusoutput(git+"log -1 --format=%h FETCH_HEAD")
        fulllog = fulllog != 0
        if not fulllog: print("* current revision is "+old)
        else: print("* no revisions available")
        if os.system(git+"fetch web master") != 0:
            print("* an error occured during fetch")
            exit(1)
        new = getoutput(git+"log -1 --format=%h FETCH_HEAD")
        if not fulllog: print("* fetched revision is "+old)
        if old != new or fulllog:
            print("* get filenames from log")
            if fulllog:log = getoutput(git+"log --name-only --format=%n FETCH_HEAD")
            else: log = getoutput(
                    "{0}log --name-only --format=%n {1}..{2}".\
                    format(git,old,new))
        else:
            print("* no new updates")
            if not update_all: exit()

    while "\n\n" in log: log = log.replace("\n\n","\n").split("\n")
    files = []

    for line in log:
        m = re_news.match(line)
        if m is not None:
            filename = m.group('file')
            if filename not in files: files.append(filename)

    if files:
        print("* load files from git")
        os.system(git+"checkout --merge FETCH_HEAD -- "+" ".join(files))
    else:
        files = list(map(lambda fn:"content/news/"+fn, os.listdir("content/news/")))

    for filename in files:
        if debug:
            print("* try to add to db:  "+filename)
            data = load_file(filename)
        else:
            try:
                data = load_file(filename)
                print("* add to db:  "+filename)
            except:
                data = None
                print("\033[31m* errör during parsing:  "+filename+"\033[m")
        if data:
            try:
                old = Episode.find().filter_by(filename = filename).one()
                File.find().filter_by(episode = old.id).delete()
                Link.find().filter_by(episode = old.id).delete()
            except: old = 0
            episode = Episode(filename=filename, **data['episode'])
            episode.save()
            if old:
                Comment.find().filter_by(episode=old.id).update({'episode':episode.id})
                Episode.find().filter_by(id = old.id).delete()
            list(map(lambda kwargs: File(episode=episode.id, **kwargs).add(), data['files']))
            list(map(lambda kwargs: Link(episode=episode.id, **kwargs).add(), data['links']))
            session().commit()
    print("done.")

if __name__ == "__main__":
    main()