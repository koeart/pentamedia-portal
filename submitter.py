#!/usr/bin/env python3.0
from os.path import join as pjoin
from juno import init, redirect, route, run, get, \
                 model, post, \
                 subdirect, template, autotemplate
init({'static_url':'/s/*:file', '500_traceback':True, 'use_templates':True,
  'use_db':True,
  'template_kwargs':{'extensions':["jinja2.ext.do","jinja2.ext.loopcontrols"]}})

# routes

@route('/')
def index(web):
  print(web)
  return template("submitter.tpl", header_color="ffc8b4",
           sections=[("Episodes","/radio"),
                     ("Login",pjoin(web.location,"login")),
                     ("Register",pjoin(web.location,"register"))])




# run

run()

