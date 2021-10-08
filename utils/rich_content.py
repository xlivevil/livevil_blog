import re

from markdown import Markdown
from markdown.extensions.toc import TocExtension, slugify_unicode


def generate_rich_content(value) -> dict[str, str]:

    md = Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.admonition',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify_unicode),
        ]
    )
    content = md.convert(value)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    toc = m.group(1) if m is not None else ''
    return {'content': content, 'toc': toc}
