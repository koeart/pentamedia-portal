{% from "captcha.tpl" import captchas_begin, captchas_body, captchas_end with context %}
<!DOCTYPE HTML>
<html>
  <head>
    <title>pentamedia{{title|default("")}}</title>
    {% if not fail|d(False) %}
    <link href="/{{site}}/{{episode.link}}/comments.atom" type="application/atom+xml" rel="alternate" title="Comments Feed" />
    {% endif %}
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
<div class="content">
{% block htmlrts %}

<div class="rating">
{% if not fail|d(False) %}
{% if not hide_rating_detail|d(False) %}

<div style="margin-left:1em" id="rating-detail">
  {{rating.stars}} &nbsp; {{rating.score|round(2,'floor')}} by {{rating.count}} Vote{% if rating.count != 1 %}s{% endif %}
</div>

{% else %}

<div style="font-size:2em">{{rating.stars}}</div>
<div style="margin-left:1em">
  {{rating.score|round(2,'floor')}} by {{rating.count}} Vote{% if rating.count != 1 %}s{% endif %}
</div>

{% endif %}
{% if rating_form|d(False) %}

{% macro action() -%}
/{{site}}/{{episode.link}}/rating/new{{''|d('.json',isjson|d(False))}}
{%- endmacro %}

{{captchas_begin(action())}}
<p class="scores">
{% for n, star in enumerate(rating.stars) %}
<input type="radio" name="score" value="{{n+1}}" id="score{{n+1}}"/>{{star}}
{% endfor %}
</p>
{{captchas_body()}}
{{captchas_end("I like it that much!")}}

{% else %}
{% if isjson is not defined
%}<p>✰ <a href="/{{site}}/{{episode.link}}/rate#new" class="add_comment add_rating">new Rating…</a></p>{% endif %}
{% endif %}
{% endif %}
</div>
{% endblock %}
</div>

  </body>
</html>

{% macro print_rating() -%}
{{self.htmlrts()}}
{%- endmacro %}