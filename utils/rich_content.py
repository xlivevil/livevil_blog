import re

import markdown
from markdown.extensions.toc import TocExtension, slugify


def generate_rich_content(value):

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.admonition',
        
        TocExtension(slugify=slugify),
    ])
    content = md.convert(value)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    toc = m.group(1) if m is not None else ''
    return {"content": content, "toc": toc}
