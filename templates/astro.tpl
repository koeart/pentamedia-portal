<!DOCTYPE HTML>
<html>
  <head>
    <title>pentamedia{{title|default("")}}</title>
    <link href="/{{site}}/{% if episode is defined %}{{episode.link}}/{% endif %}comments.atom" type="application/atom+xml" rel="alternate" title="Comments Feed" />
    {% if episode is defined %}<link type="text/xml" href="/trackback/{{episode.id}}" title="Pentamedia Trackback"/>{% endif %}
    <link rel="SHORTCUT ICON" href="/img/c3d2.ico" type="image/x-icon">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
{% set csss = csss|default([]) %}
{% if "style" not in csss %}
  {% do csss.append("style") %}
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
    <ul class="headlinks">
      <li><a href="http://pentamedia.c3d2.de/submit/">News Submitter</a></li>
      <li><a href="http://www.hq.c3d2.de/pentastats">Statistiken</a></li>
      <li><a href="http://twitter.com/pentaradio">@pentaradio</a></li>
      <li><a href="http://c3d2.de">C3D2</a></li>
      <li><a href="http://c3d2.de/muc.html">Chat</a></li>
    </ul>
    <h1><a title="Alles" href="/" style="border:none;color:transparent;z-index:42;"><img src="/img/pentamedia_text.png"></a></h1>
    <ul class="categories">
      <li><a title="Alles" href="/">*</a></li>
      <li{% if site == "pentaradio" %} class="selected"{% endif %}><a href="/pentaradio">Pentaradio</a></li>
      <li{% if site == "pentacast" %} class="selected"{% endif %}><a href="/pentacast">Pentacast</a></li>
      <li{% if site == "pentamusic" %} class="selected"{% endif %}><a href="/pentamusic">Pentamusic</a></li>
      <li><a href="/spenden">Spenden</a></li>
    </ul>
    <div class="content">
{% block body %}
{{lipsum()}}
{% endblock %}
    </div>
<div align="center">
<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/3.0/de/"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by-nc-nd/3.0/de/88x31.png" /></a><br /><span xmlns:dc="http://purl.org/dc/elements/1.1/" href="http://purl.org/dc/dcmitype/Sound" property="dc:title" rel="dc:type">Alle Podcasts</span> von <a xmlns:cc="http://creativecommons.org/ns#" href="pentamedia.org" property="cc:attributionName" rel="cc:attributionURL">C3D2</a> stehen unter einer <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/3.0/de/">CC-BY-NC-ND</a>.
</div>
  </body>
</html>
