
from markdown import Markdown
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor

from inc.re import re_url, re_anchor

# markdown stuff

class LinkPreprocessor(Preprocessor):
    def run(self, lines):
        def parse(x): return "[{0}]({0})".format(x.group())
        def sub(line): return re_url.sub(parse, line)
        return list(map(sub, lines))

class LinkPostprocessor(Postprocessor):
    def run(self, text):
        def parse(x): return '<span class="line">{1}</span>{2}'.\
                            format(*parse_url(x.group()))
        def classify(x): return '{0} class="line"{1}'.format(*x.groups())
        text = re_anchor.sub(classify, text)
        return re_url.sub(parse, text)

md = Markdown(
              safe_mode     = 'escape',
              output_format = 'xhtml1'
             )

md.preprocessors.add("url", LinkPreprocessor(md), "_begin")
md.postprocessors.add("url", LinkPostprocessor(md), "_end")

# helper


def parse_url(url):
    domain = url.split(':',1)[1][2:].split('/',1)
    if len(domain) == 1: domain, rest = domain[0], ""
    else:
        domain, rest = domain
        if not rest == "": rest = "/{0}".format(rest)
    if domain.startswith('www.'): domain = domain[4:]
    return (url, domain, rest)

