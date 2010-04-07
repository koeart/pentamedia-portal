#!/usr/bin/env python3.0
from juno import init, redirect, route, run, get, \
                 subdirect, template, autotemplate
init({'static_url':'/s/*:file', '500_traceback':True, 'use_templates':True, 'bind_address':'',
  'template_kwargs':{'extensions':["jinja2.ext.do","jinja2.ext.loopcontrols"]}})

# routes

autotemplate("/","start.html", css="start")

@route("radio")
def radio(web):
  return template("radio.tpl",header_color="ffc8b4")#,css="cast")
  
@route("cast")
def cast(web):
  return template("cast.tpl",header_color="b4c8ff")#,css="cast")
  
@route("music")
def music(web):
  return template("music.tpl",header_color="c8ffc8")#,css="cast")



@route("sendung")
def music(web):
  return template("sendung.tpl",header_color="c8ffc8",css="sendung")


# run

run()

