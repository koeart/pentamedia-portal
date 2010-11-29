<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <author>
    <name>k-ot</name>
  </author>
  <title>{{title}}</title>
  <id>averyuniqid:D</id>
  {% if comments|d([]) != [] %}<updated>{{comments[-1].date}}</updated>{% endif %}

  {% for entry in comments|d([]) %}
  <entry>
    <link href="{{pentamediaportal}}/{{episodes[entry.episode].category}}/{{episodes[entry.episode].link}}"/>
    <id>{{entry.id}}</id>
    <updated>{{entry.date}}</updated>
    {% if entry.reply is defined %}
    <title>Comment by {{entry.author}} on {{episodes[entry.episode].name}}</title>
    <summary>{{entry.author}} added these pithy words on {{entry.fdate()}}</summary>
    {% else %}
    <title>Trackback by {{entry.title or "---"}} on {{episodes[entry.episode].name}}</title>
    <summary>{{entry.title or "---"}} by {{entry.name or "Unknown"}} on {{entry.fdate()}}</summary>
    {% endif %}
    <content type="xhtml"><div xmlns="http://www.w3.org/1999/xhtml">{{entry.text}}</div></content>
  </entry>
  {% endfor %}
</feed>
