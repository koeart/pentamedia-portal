#!/usr/bin/env python3.0
from os.path import join as pjoin
from juno import init, redirect, route, run, get, \
                 model, post, \
                 subdirect, template, autotemplate
init({'static_url':'/s/*:file', '500_traceback':True, 'use_templates':True,
  'use_db':True, 'use_sessions':True,
  'template_kwargs':{'extensions':["jinja2.ext.do","jinja2.ext.loopcontrols"]}})

#constants

sections = [("Episodes","/radio"),
            ("Login","login")]
header_color = "ffc8b4"
default = {'sections':sections, 'header_color':header_color}

# routes

@route('/')
def index(web):
  return template("submitter.tpl", **default)

@route('login')
def login(web):
  return template("login.tpl", **default)

# run

run()

