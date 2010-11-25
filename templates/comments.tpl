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
{% block htmlcmts %}
<div class="comments">
<p>{% set comments = comments|d([]) %}{{comments|count}} Comment{{comments|count != 1 and "s" or ""}}</p>
{% if not fail|d(False) %}
{% if isjson|d(False) %}
<style type="text/css">
.comment {
  font-size: 0.9em;
  margin-bottom: 1em;
}
.comment a {
  border: none;
  color: #555555;
}
.comment a:hover { text-decoration: none; border: none; }
.comment a:hover .line { text-decoration: underline; }
.comment .line:hover { text-decoration: underline; }
.comment .author {
  font-size: small;
  font-style: italic;
  font-weight: bold;
  margin-left: 1em;
}
</style>
{%endif%}
{% for comment in comments %}
  <div class="comment" style="border:none;background:none{% if comment.reply != -1 %};margin-left:{{comment.level}}em;border-left:4px solid #ddd{% endif %};">{{comment.text}}
    <small class="author"><a href="/{{site}}/{{episode.link}}{{''|d('/comments',isjson|d(False))}}/reply?{{comment.id}}#new" class="line">{{comment.author|trim|e}}</a></small>
    <small> added these pithy words on {{comment.fdate()}}</small>
  </div>
{% endfor %}
{% if comment_form|d(False) %}
<form action="/{{site}}/{{episode.link}}/comment/new{{''|d('.json',isjson|d(False))}}" method="post" id="new">
<input type="hidden" name="hash" value="{{hash}}" />
<input type="hidden" name="reply" value="{{reply}}" />
    <p>
       <label for="author">Name</label> (required)<br>

      <input type="text" name="author" id="author" class="textarea" value="" size="15" tabindex="1" />

     </p>

    <fieldset>
      <legend>
	<input type="radio" name="tcha" value="sum" id="sumtcha"/>
	<label for="sumtcha">Sumtcha</label>
      </legend>
      <p>
	Enter the sum of {{a}}, {{b}} and {{c}}:
	<input type="text" name="sumtcha" id="sumtcha" value="" size="3" tabindex="2" />
      </p>
    </fieldset>
    <fieldset>
      <legend>
	<input type="radio" name="tcha" value="cat" checked="checked" id="cattcha"/>
	<label for="cattcha">Cattcha</label>
      </legend>
      <p>
	<input type="checkbox" name="cat" value="A" /><img src="/cat/A?{{hash}}" />
	<input type="checkbox" name="cat" value="B" /><img src="/cat/B?{{hash}}" /><br />
	<input type="checkbox" name="cat" value="C" /><img src="/cat/C?{{hash}}" />
	<input type="checkbox" name="cat" value="D" /><img src="/cat/D?{{hash}}" />
      </p>
    </fieldset>
    <p>
      <label for="comment">Your Comment</label>
    <br />
      <textarea name="comment" style="border: 1px solid #000;" id="comment" cols="50" rows="6" tabindex="4">{{at_author}}</textarea>
      <br /><a href="http://en.wikipedia.org/wiki/Markdown">Markdown</a> enabled. (url autolinking included.)
</p>
<input name="submit" id="submit" type="submit" tabindex="5" value="Say It!" style="position:absolute;margin-left:29em;" />


    </form>
{% else %}
{% if isjson is not defined %}<a href="/{{site}}/{{episode.link}}/comment#new" class="add_comment">new Comment …</a>{% endif %}
{% endif %}
{% endif %}
</div>
{% endblock %}
</div>

  </body>
</html>

{% macro print_comments() -%}
{{self.htmlcmts()}}
{%- endmacro %}