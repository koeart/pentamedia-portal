#!/usr/bin/env python3.0
from juno import init, redirect, route, run, get, \
                 subdirect, template, autotemplate
init({'static_url':'/s/*:file', '500_traceback':True, 'use_templates':True, 'bind_address':'',
  'template_kwargs':{'extensions':["jinja2.ext.do","jinja2.ext.loopcontrols"]}})

#constants

head_colors = {'radio':"ffc8b4", 'cast':"b4c8ff", 'music':"c8ffc8"}

# routes

autotemplate("/","start.html", css="start")

@route("radio")
def radio(web):
  return template("radio.tpl",header_color=head_colors['radio'])
  
@route("cast")
def cast(web):
  return template("cast.tpl",header_color=head_colors['cast'])
  
@route("music")
def music(web):
  return template("music.tpl",header_color=head_colors['music'])



@route("/:star/sendung")
def sendung(web,star):
  return template("sendung.tpl",header_color=head_colors[star],css="sendung")


# run

run()

