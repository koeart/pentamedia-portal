<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <author>
    <name>k-ot</name>
  </author>
  <title>Pentamedia-Portal // {{episode.name}} // Comments</title>
  <id>averyuniqid:D</id>
  {% if comments|d([]) != [] %}<updated>comments[-1].date</updated>{% endif %}

  {% for comment in comments|d([]) %}
  <entry>
    <title>Comment by {{comment.author}} on {{episode.name}}</title>
    <link href="http://pentamedia.hq.c3d2.de/{{site}}/{{episode.link}}"/>
    <id>{{comment.id}}</id>
    <updated>{{comment.date}}</updated>
    <summary>{{comment.author}} added these pithy words on {{comment.fdate()}}</summary>
    <content>{{comment.text}}</content>
  </entry>
  {% endfor %}
</feed>
