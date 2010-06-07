
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
