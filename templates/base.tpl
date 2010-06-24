<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="de" xml:lang="de">
  <head>
    <title>pentamedia{{title|default("")}}</title>
    <link rel="SHORTCUT ICON" href="/img/c3d2.ico" type="image/x-icon">
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
    <link rel="stylesheet" title="Default" type="text/css" href="/css/{{css_file}}.css" />
{% endfor %}
  </head>
  <body>
<div id="header"{% if header_color is defined %} style="background-color:#{{header_color}};"{% endif %}>
<div class="header_link"><a href="/" alt="Start">Start</a><a href="/archiv" alt="Archiv">Archiv</a></div>
<div class="buttons">
<div class="button"><a href="/radio" alt="Pentaradio"><img src="/img/pentaradio.png" alt="Pentaradio" /></a></div>
<div class="button"><a href="/cast" alt="Pentacast"><img src="/img/pentacast.png" alt="Pentacast" /></a></div>
<div class="button"><a href="/music" alt="Pentamusic"><img src="/img/pentamusic.png" alt="Pentamusic" /></a></div>
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
<div align="center">
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/de/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-nc-sa/3.0/de/88x31.png" /></a><br /><span xmlns:dc="http://purl.org/dc/elements/1.1/" href="http://purl.org/dc/dcmitype/Sound" property="dc:title" rel="dc:type">pentaMedia</span> von <a xmlns:cc="http://creativecommons.org/ns#" href="pentamedia.org" property="cc:attributionName" rel="cc:attributionURL">C3D2</a> steht unter einer <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/de/">Creative Commons Namensnennung-Keine kommerzielle Nutzung-Weitergabe unter gleichen Bedingungen 3.0 Deutschland Lizenz</a>.
</div>
  </body>
</html>
