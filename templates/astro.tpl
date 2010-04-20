<!DOCTYPE HTML>
<html>
  <head>
    <title>pentamedia{{title|default("")}}</title>
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
      <li><a href="#">Nachrichtendienst</a></li>
      <li><a href="#">Feedbackzentrale</a></li>
      <li><a href="#">Statistiken</a></li>
      <li><a href="#">C3D2</a></li>
    </ul>
    <h1>Pentamedia</h1>
    <ul class="categories">
      <li><a title="Alles" href="/">*</a></li>
      <li{% if site == "radio" %} class="selected"{% endif %}><a href="/radio">Pentaradio</a></li>
      <li{% if site == "cast" %} class="selected"{% endif %}><a href="/cast">Pentacast</a></li>
      <li{% if site == "music" %} class="selected"{% endif %}><a href="/music">Pentamusic</a></li>
      <li><a href="#">Misc</a></li>
    </ul>

    <div class="content">
{% block body %}
{{lipsum()}}
{% endblock %}
    </div>

  </body>
</html>
