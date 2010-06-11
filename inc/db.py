from datetime import datetime
from juno import model

# models

File = model('File',
             episode = 'integer',
             info    = 'string',
             name    = 'string',
             type    = 'string',
             link    = 'string'
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

# helper

def _fdate(date:datetime):
    return date.strftime("%A, %d. %B %Y um %H:%M")

