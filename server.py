#!/usr/bin/env python3.0
from juno import init, run

init({'static_url':      '/(s/)?(?P<file>(?<=s/).*|(css|img|js)/.*)',
      '500_traceback':   True,
      'use_templates':   True,
      'bind_address':    '',
      'use_db':          True,
      'db_location':     "db.sqlite",
      'template_kwargs':
         {'extensions':  ["jinja2.ext.do","jinja2.ext.loopcontrols"]}
     })

import inc.routes

run()
