{% extends "base.tpl" %}

{% block body %}
<div class="submitarea">
  <form action="submit" method="post" id="submitform">
    <textarea name="blob" id="blob" cols="42" rows="2" tabindex="1"></textarea>
    <input name="submit" id="submit" type="submit" tabindex="2" value="add this!" />
	</form>
</div>
<br/>
<div class="news_table">
<div class="news_row">
<div class="news">
{% for entry in entries() %}<div class="entry"><h3 class="title"><a href="{{entry.url}}">{{entry.title|e}}</a></h3><small class="description">{{entry.description|e}}</small><div class="excerpt">{{entry.excerpt|e}}</div></div>{% endfor %}
</div>
<div class="tagcloud">
tagcloud
</div>
</div>
</div>
{% endblock %}
