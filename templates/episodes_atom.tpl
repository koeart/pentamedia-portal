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
    <link href="{{pentamediaportal}}/{{episode.category}}/{{episode.link}}"/>
    <id>{{episode.id}}</id>
    <updated>{{episode.date}}</updated>
    <title>{{episode.name}}</title>
    <summary><div xmlns="http://www.w3.org/1999/xhtml">{{episode.short}}</div></summary>
    <content type="xhtml"><div xmlns="http://www.w3.org/1999/xhtml">{{episode.long}}</div></content>
  </entry>
  {% endfor %}
</feed>
