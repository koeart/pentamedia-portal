<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="de" xml:lang="de">
  <head>
    <title>pentamedia{{title|default("")}}</title>
    <link rel="SHORTCUT ICON" href="/s/c3d2.ico" type="image/x-icon">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
{% set csss = csss|default([]) %}
{% if "base" not in csss %}
  {% do csss.append("base") %}
{% endif %}
{% if css is defined %}
  {% if css not in csss %}
    {% do csss.append(css) %}
  {% endif %}
{% endif %}
{% for css_file in csss %}
    <link rel="stylesheet" title="Default" type="text/css" href="/s/{{css_file}}.css" />
{% endfor %}
  </head>
  <body>
<div id="header"{% if header_color is defined %} style="background-color:#{{header_color}};"{% endif %}>
<div class="header_link"><a href="/" alt="Start">Start</a><a href="/archiv" alt="Archiv">Archiv</a></div>
<div class="buttons">
<div class="button"><a href="/radio" alt="Pentaradio"><img src="/s/pentaradio.png" alt="Pentaradio" /></a></div>
<div class="button"><a href="/cast" alt="Pentacast"><img src="/s/pentacast.png" alt="Pentacast" /></a></div>
<div class="button"><a href="/music" alt="Pentamusic"><img src="/s/pentamusic.png" alt="Pentamusic" /></a></div>
</div>
</div>
<div class="links">
  {% set sections = sections|d([]) %}
  {{sections|count == 0 and "&nbsp;" or ""}}
  {% for link,url in sections %}
    <a href="{{url}}" class="section">{{link}}</a>
  {% endfor %}
</div>
<div class="content">
{% block body %}
{{lipsum()}}
{% endblock %}
</div>
  </body>
</html>
