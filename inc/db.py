from datetime import datetime
from juno import model

# models

File = model('File',
             episode = 'integer',
             info    = 'string',
             name    = 'string',
             type    = 'string',
             mime    = lambda self: _mime(self),
             typecat = lambda self: self.type.partition("/")[0],
             typetyp = lambda self: self.type.partition("/")[2],
             link    = 'string'
            )

Preview = model('Preview',
                episode  = 'integer',
                link     = 'string',
                static   = 'string',
                animated = 'string'
               )

Link = model('Link',
             episode = 'integer',
             title   = 'string',
             url     = 'string'
            )

Episode = model('Episode',
                filename = 'string',
                name     = 'string',
                link     = 'string',
                category = 'string',
                author   = 'string',
                date     = 'datetime',
                fdate    = lambda self: _fdate(self.date),
                ismedia  = lambda self: _ismedia(self.files or []),
                short    = 'text',
                long     = 'text'
               )

Comment = model('Comment',
                episode = 'integer',
                author  = 'string',
                reply   = 'integer',
                date    = 'datetime',
                fdate   = lambda self: _fdate(self.date),
                text    = 'text'
               )

Trackback = model('Trackback',
                  episode = 'integer',
                  title   = 'string',
                  text    = 'text',
                  url     = 'string',
                  date    = 'datetime',
                  fdate   = lambda self: _fdate(self.date),
                  name    = 'string'
                 )

ShownoteTrackback = model("ShownoteTrackback",
                          filename = 'string',
                          url      = 'string'
                         )

Rating = model ("Rating",
                episode = 'integer',
                score   = 'integer'
               )

# helper

def _fdate(date:datetime):
    return date.strftime("%A, %d. %B %Y um %H:%M")

def _mime(file):
    if "torrent" in file.type:
        return "bittorrent"
    elif "multipart" in file.type:
        return "pkg"
    return file.typecat()

def _ismedia(files):
    mimes = list(map(lambda f:f.typecat(), files))
    return "video" in mimes or "audio" in mimes
