#!/usr/bin/env python3

# CONFIG

update_all = True
debug      = False
trackback  = True
# ------

import re
import os
import os.path as ospath
from subprocess import getoutput, getstatusoutput
from inc.cwebparser import load_file
from juno import init, session

init({'use_db':          True,
      'db_location':     "db.sqlite"
     })

from inc.db import File, Link, Episode, Comment, ShownoteTrackback
from inc.trackback import trackback_client
from inc.progressbar import Progressbar
from config import pentamediaportal

re_news = re.compile(r"(?P<file>content/news/penta(cast|music|radio).*\.xml)")
gitcmd = "git --git-dir=cweb.git --work-tree=. "


def git(options, verbose=0):
    if   verbose == 0: # state
        return os.system(gitcmd + options)
    elif verbose == 1: # output
        return getoutput(gitcmd + options)
    elif verbose == 2: # status & output
        return getstatusoutput(gitcmd + options)
    else:
        print("U doing it wrong.")


def main():
    log = ""
    links_count, tb_count, skip_count, error_count = 0, 0, 0, 0

    git_test = getoutput("git log --format=%n")
    if "fatal" in git_test or "--format" in git_test:
        print("ERROR: your git version is to old.")
        os.system("git --version")
        exit(1)

    if not os.path.exists("cweb.git"):
        print("* no c3d2-web git repository found")
        os.mkdir("cweb.git")
        git("init")
        git("remote add web git://194.77.75.60/c3d2-web/git.git")
        if git("fetch web master") == 0:
            git("branch --track master FETCH_HEAD")
            print("* get filenames from log")
            log = git("log --name-only --format=%n",1)
        else:
            print("* an error occured during fetch")
            exit(1)
    else:
        print("* fetching updates")
        createbranch = "master" not in git("branch",1)
        if createbranch:
            print("* guessing error at initial fetch")
            fulllog, old = False, ""
        else:
            fulllog, old = git("log -1 --format=%h",2)
            fulllog = fulllog != 0
        if not fulllog: print("* current revision is",old)
        else: print("* no revisions available")
        if git("fetch web master") != 0:
            print("* an error occured during fetch")
            exit(1)
        if createbranch: git("branch --track master FETCH_HEAD")
        git("update-ref HEAD FETCH_HEAD")
        new = git("log -1 --format=%h",1)
        if not fulllog: print("* fetched revision is",new)
        if old != new or fulllog:
            print("* get filenames from log")
            if fulllog:log = git("log --name-only --format=%n",1)
            else: log = git("log --name-only --format=%n {0}..{1}".\
                            format(old,new),1)
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
        git("checkout --merge master -- "+" ".join(files))
    else:
        files = list(map(lambda fn:"content/news/"+fn, os.listdir("content/news/")))

    for filename in files:
        if debug:
            print("* try to add to db: ",filename)
            data = load_file(filename)
        else:
            try:
                data = load_file(filename)
            except:
                data = None
                print("\033[31m* errör during parsing: ",filename,"\033[m")
        if data:
            olds = Episode.find().filter_by(filename = filename).all()
            for old in olds:
                try:
                    File.find().filter_by(episode = old.id).delete()
                    Link.find().filter_by(episode = old.id).delete()
                except Exception as e: print("\033[31merrör 1:\033[m",e)
            episode = Episode(filename=filename, **data['episode'])
            episode.save()
            if olds:
                for old in olds:
                    try:
                        Comment.find().filter_by(episode=old.id).update({'episode':episode.id})
                        Episode.find().filter_by(id = old.id).delete()
                    except Exception as e: print("\033[31merrör 2:\033[m",e)
                print("\033[32m* update db: ",filename,"\033[m")
            else: print("\033[32m* add to db: ",filename,"\033[m")
            list(map(lambda kwargs: File(episode=episode.id, **kwargs).add(), data['files']))
            list(map(lambda kwargs: Link(episode=episode.id, **kwargs).add(), data['links']))
            if trackback:
                links_count += len(data['links'])
                pb = Progressbar(0, len(data['links']), 42, True)
                for n, linkdata in enumerate(data['links']):
                    link = linkdata['url']
                    pb.update(n, link)
                    used = ShownoteTrackback.find().filter_by(url = link).count()
                    if not used:
                        response = trackback_client(link,
                                        pentamediaportal+"/{0}/{1}".\
                                         format(episode.category, episode.link),
                                        title = episode.name,
                                        excerpt = episode.short
                                                )
                        if response:
                            response = response.replace(" ","")
                            response = response.replace("\n","")
                            response = response.lower()
                            print(link, response)
                            tb_count += 1
                            if "<error>0</error>" in response:
                                ShownoteTrackback(
                                    filename = filename,
                                    url      = link).add()
                            else: error_count += 1
                    else:
                        tb_count += 1
                        skip_count += 1
                    pb.draw()
                pb.clear()
            session().commit()
    if trackback:
        print("{0} Shownotes scaned. {1} Trackback links discovered. {2} skipped. {3} failed to use.".\
              format(links_count, tb_count, skip_count, error_count))
    print("done.")

if __name__ == "__main__":
    main()
