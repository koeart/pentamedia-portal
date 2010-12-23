#!/usr/bin/env python3

import re
import os
import os.path as ospath
from copy import deepcopy
from optparse import OptionParser
from subprocess import getoutput, getstatusoutput
from inc.cwebparser import load_podcast_file,  \
                           load_recording_file, \
                           get_category, flatten_files
from juno import init, session

init({'use_db':          True,
      'db_location':     "db.sqlite"
     })

from inc.db import File, Link, Episode, Comment, Rating, Preview,\
                   ShownoteTrackback
from inc.trackback import trackback_client
from inc.progressbar import Progressbar
from inc.console import style, drug
from config import pentamediaportal, cwebgitrepository, cwebnewsfolder
from blacklist import sites as blacklist

re_news = re.compile(r"(?P<status>M|A|D)\s*(?P<file>"+cwebnewsfolder+r"((penta(cast|music|radio))|(d(s|atenspuren))).*\.xml)")
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


def check_git_version():
    git_test = getoutput("git log --format=%n")
    if "fatal" in git_test or "--format" in git_test:
        print("ERROR: your git version is to old.")
        os.system("git --version")
        exit(1)


def fetch_log_from_git(update_all=False):
    log = ""

    if not os.path.exists("cweb.git"):
        print("* no c3d2-web git repository found")
        os.mkdir("cweb.git")
        git("init")
        git("remote add web " + cwebgitrepository)
        if git("fetch web master") == 0:
            git("branch --track master FETCH_HEAD")
            print("* get all filenames from log")
            log = git("log --name-status --format=%n",1)
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
        fulllog = fulllog or update_all
        if git("fetch web master") != 0:
            print("* an error occured during fetch")
            exit(1)
        if createbranch: git("branch --track master FETCH_HEAD")
        git("update-ref HEAD FETCH_HEAD")
        new = git("log -1 --format=%h",1)
        if not fulllog: print("* fetched revision is",new)
        if old != new or fulllog:
            if fulllog:
                print("* get all filenames from log")
                log = git("log --name-status --format=%n",1)
            else:
                print("* get updated filenames from log")
                log = git("log --name-status --format=%n {0}..{1}".\
                          format(old,new),1)
        else:
            print("* no new updates")
            if not update_all: exit()

    return log


def is_recording_file(filename):
    lines = getoutput("grep '<resource' ./"+filename)
    return len(lines) > 0


def clean_log(log):
    while "\n\n" in log: log = log.replace("\n\n","\n").split("\n")
    return log


def get_filenames_from_gitlog(log, update_all=False):
    files, deleted, log = [], [], clean_log(log)
    print("* filter filenames")
    for line in log:
        m = re_news.match(line)
        if m is not None:
            filename = m.group('file')
            status = m.group('status')
            if status == "D":
                print(style.yellow+"* skip",filename,
                    "(file deleted)", style.default)
                deleted.append(filename)
                continue
            if filename not in deleted and filename not in files:
                files.append(filename)

    if files:
        print("* load files from git")
        git("checkout --merge master -- "+" ".join(files))
    elif update_all:
        print("* load files from folder")
        files = list(map(lambda fn:cwebnewsfolder+fn, os.listdir(cwebnewsfolder)))

    return files


class Trackbacker():
    def __init__(self, enabled):
        self.count = drug(links = 0, tb = 0, skip = 0, error = 0, ign = 0)
        self.disabled = not enabled

    def send(self, episode, link):
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
            self.count.tb += 1
            if "<error>0</error>" in response:
                ShownoteTrackback(
                    filename = filename,
                    url      = link).add()
            else: self.count.error += 1

    def check_all(self, episode, links):
        if self.disabled or not links: return
        self.count.links += len(links)
        pb = Progressbar(0, len(links), 42, True)
        for n, linkdata in enumerate(links):
            link = linkdata['url']
            blacklisted = False
            for site in blacklist:
                if site in link:
                    blacklisted = True
                    break
            if not blacklisted: pb.update(n, link)
            used = ShownoteTrackback.find().filter_by(url = link).count()
            if not blacklisted and not used:
                self.send(episode, link)
            else:
                if blacklisted: self.count.ign += 1
                else:
                    self.count.tb += 1
                    self.count.skip += 1
            if not blacklisted: pb.draw()
        pb.clear()

    def print_stats(self):
        if self.disabled: return
        print(("{0} Shownotes scaned. {4} ignored. " + \
              "{1} Trackback links discovered. " + \
              "{2} skipped. {3} failed to use.").\
              format(self.count.links, self.count.tb, self.count.skip,\
                    self.count.error, self.count.ign))


def save_in_database(filename, data, tracker):
    olds = Episode.find().filter_by(filename = filename).all()
    for key in ['files', 'links', 'previews']:
        if key not in data:
            data[key] = []
    for old in olds:
        try:
            Link.find().filter_by(episode = old.id).delete()
            File.find().filter_by(episode = old.id).delete()
            Preview.find().filter_by(episode = old.id).delete()
        except Exception as e: print(style.red+"errör 1:"+style.default,e)
    episode = Episode(filename=filename, **data['episode'])
    episode.save()
    for old in olds:
        try:
            Comment.find().filter_by(episode=old.id).update({'episode':episode.id})
            Rating.find().filter_by(episode=old.id).update({'episode':episode.id})
            Episode.find().filter_by(id = old.id).delete()
        except Exception as e: print(style.red+"errör 2:"+style.default,e)
    if olds: print(style.green+"* update db: ",filename,style.default)
    else: print(style.green+"* add to db: ",filename,style.default)
    list(map(lambda kwargs: File(episode=episode.id, **kwargs).add(), data['files']))
    list(map(lambda kwargs: Preview(episode=episode.id, **kwargs).add(), data['previews']))
    list(map(lambda kwargs: Link(episode=episode.id, **kwargs).add(), data['links']))
    tracker.check_all(episode, data['links'])
    session().commit()


def save_recording_in_database(filename, data, tracker):
    # datastructure:
    # xml-file as Episode (category='ds*') with files from resource-tags
    # files from resource-tags as Episodes (category='file/ds*/:link')
    #    with self and alternatives as files
    dsfiles = deepcopy(data['files'])
    for f in data['files']:
        f.pop('alternatives')
    try:
        olds = Episode.find().filter_by(filename = filename).all()
        old_files = list(map(lambda f: f.link,
            sum(map(lambda o: File.find().\
            filter_by(episode = o.id).all(), olds), [])))
    except Exception as e: print(style.red+"errör 0:"+style.default,e)
    save_in_database(filename, data, tracker)
    for dsfile in dsfiles:
        dsdata = deepcopy(data)
        alternatives = dsfile.pop('alternatives')
        dsdata['files'] = [dsfile] + alternatives
        dsepisode = dsdata['episode']
        dsepisode['name'] = dsfile['name']
        dsepisode['long'] = dsfile['info']
        dsepisode['link'] = ospath.basename(dsfile['link']).\
            replace(" ", "_").replace("%20", "_")
        dsepisode['short'] = dsfile['type']
        dsepisode['category'] = "file/{0}/{1}".\
            format(data['episode']['category'], data['episode']['link'])
        save_in_database(dsfile['link'], dsdata, tracker)
        if dsfile['link'] in old_files:
            old_files.remove(dsfile['link'])
        for alternative in alternatives:
            if alternative['link'] in old_files:
                old_files.remove(alternative['link'])
    if old_files:
        episode = Episode.find().filter_by(filename = filename).one()
    for old_file in old_files:
        print(style.red + style.bold +
            "* found dangling file (link: {0})".\
            format(old_file), "move comments and rating to",
            "[id:{0}, link:{1}, name:{2}]".\
            format(episode.id,episode.link,episode.name), style.default)
        try:
            olds = Episode.find().filter_by(filename = old_file).\
                filter(Episode.category.startswith("file/")).all()
            if debug: print("* found",len(olds),"episodes to delete")
            for old in olds:
                Comment.find().filter_by(episode=old.id).update({'episode':episode.id})
                Rating.find().filter_by(episode=old.id).update({'episode':episode.id})
            print("* deleted {0} episodes".format(
                Episode.find().filter_by(filename = old_file).delete()))
        except Exception as e: print(style.red+"errör 3:"+style.default,e)
        session().commit()


def fill_database(files, debug=False, trackback=False):
    tracker = Trackbacker(trackback)
    for filename in files:
        category = get_category(filename)
        if not category or ("penta" not in category and "ds" not in category):
                print(style.red+"* errör can't categorize ",
                    filename, "  found:", category, style.default)
                continue # proceed with next
        if not ospath.exists("./"+filename):
            print(style.red+"* errör can't find", filename, style.default)
            continue # proceed with next
        if "penta" in category:
            load_file = load_podcast_file
        elif "ds" in category:
            load_file = load_recording_file
            if not is_recording_file(filename):
                print(style.green + style.bold + "* skip", filename,
                    "(no resources found)", style.default)
                continue # skip this file
        else:
            load_file = lambda f: print(style.magenta + \
                "* nothing happen with",f,style.default)
        if debug:
            print("* try to add to db: ",filename)
            data = load_file(filename)
        else:
            try:
                data = load_file(filename)
            except Exception as e:
                data = None
                print(style.red + "* errör during parsing",
                    filename+": ", e, style.default)
        if not data: continue

        if data['type'] == "podcast":
            save_in_database(filename, data, tracker)
        elif data['type'] == "recording":
            save_recording_in_database(filename, data, tracker)
        else:
            print(style.red+"* errör got unsupported data type:",
                data['type'], style.default)
    tracker.print_stats()


def main(update_all, debug, trackback):
    check_git_version()
    log = fetch_log_from_git(update_all)
    files = get_filenames_from_gitlog(log, update_all)
    fill_database(files, debug, trackback)
    print("done.")


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-a", "--all",
        dest="update_all", action="store_true", default = False,
        help = "update everthing again [default: %default]")
    parser.add_option("-d", "--debug",
        dest="debug", action="store_true", default = False,
        help = "show errors [default: %default]")
    parser.add_option("-t", "--no-trackback",
        dest="no_trackback", action="store_true", default = False,
        help ="disable trackback crawling [default: %default]")

    opts, _ = parser.parse_args()
    main(opts.update_all, opts.debug, not opts.no_trackback)
