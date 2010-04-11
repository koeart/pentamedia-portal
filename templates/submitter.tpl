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
{% for entry in entries() %}<div class="entry"><h3 class="title"><div class="entry_head"><div class="buttons"><a href="{{entry.url}}" class="link">{{entry.title|e}}</a><small class="button">{{entry.score}}<div class="info">Score</div></small><a href="like?{{entry.id}}" class="button">♥<div class="info">like it</div></a><a href="hate?{{entry.id}}" class="button">↯<div class="info">hate it</div></a></div></h3><small class="description">{{entry.description|e}}</small><div class="excerpt">{{entry.excerpt|e}}</div></div>{% endfor %}
</div>
<div class="tagcloud">
tagcloud
</div>
</div>
</div>
{% endblock %}
