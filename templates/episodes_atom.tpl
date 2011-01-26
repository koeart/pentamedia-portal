<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <author>
    <name>k-ot</name>
  </author>
  <title>{{title}}</title>
  <id>averyuniqid:D</id>
  {% if episodes|d([]) != [] %}<updated>{{episodes[-1].date}}</updated>{% endif %}

  {% for episode in episodes|d([]) %}
  <entry>
    <link href="{{pentamediaportal}}/{{clean_category(episode.category)}}/{{episode.link}}"/>
    <id>{{episode.id}}</id>
    <updated>{{episode.date}}</updated>
    <title>{{episode.name}}</title>
    <summary>{{remove_html(episode.short)}}</summary>
    <content>{{remove_html(episode.long)}}</content>
  </entry>
  {% endfor %}
</feed>
