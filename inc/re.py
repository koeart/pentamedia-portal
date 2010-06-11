
import re

# constants

re_reply    = re.compile(
                         r'@(\w+)'
                        )

re_url      = re.compile(
 r'(?<!"|\()((https?|ftp|gopher|file)://(\w|\.|/|\(|\)|\?|=|%|&|:|#|_|-|~|\+)+)'
                        )

re_anchor   = re.compile(
r'(<\s*a[^<>]*)(>(?!(https?|ftp|gopher|file)://)(.(?!<\s*/\s*a\s*>))*.<\s*/\s*a\s*>)'
                        )

re_trackback = re.compile(
r'(<\s*(link|a)[^<>]*)(((rel\s*=\s*[\'"](?P<rela>[^\'"]*)[\'"])([^<>]*)(href\s*=\s*[\'"](?P<urla>[^\'"]*)[\'"]))|((href\s*=\s*[\'"](?P<urlb>[^\'"]*)[\'"])([^<>]*)(rel\s*=\s*[\'"](?P<relb>[^\'"]*)[\'"])))'
                         )
