#!/usr/bin/env python3

import re
import os
import os.path as ospath
from subprocess import getoutput, getstatusoutput

re_news = re.compile(r"(?P<file>content/news/penta(cast|music|radio).*\.xml)")
git = "git --git-dir=cweb.git "

def main():
    log = ""

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
            exit()

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

    # FIXME update database with content from koeart's parser

if __name__ == "__main__":
    main()