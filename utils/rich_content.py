import re

import bleach
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


# 评论由任意登录用户提交，markdown 会原样透传内嵌 HTML，渲染前必须按白名单消毒。
# 文章正文的作者限定为管理员（可信内容），因此 Post.rich_content 不做消毒。
COMMENT_ALLOWED_TAGS = [
    'a', 'abbr', 'b', 'blockquote', 'br', 'code', 'del', 'div', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i',
    'img', 'li', 'ol', 'p', 'pre', 's', 'span', 'strike', 'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'th',
    'thead', 'tr', 'ul',
]
# codehilite 的语法高亮输出依赖 span/div 上的 class，故对所有标签放行 class
COMMENT_ALLOWED_ATTRIBUTES = {
    '*': ['class'],
    'a': ['href', 'title'],
    'img': ['src', 'alt', 'title'],
}
COMMENT_ALLOWED_PROTOCOLS = ('http', 'https', 'mailto')


def generate_comment_content(value) -> dict[str, str]:
    rich_content = generate_rich_content(value)
    rich_content['content'] = bleach.clean(
        rich_content['content'],
        tags=COMMENT_ALLOWED_TAGS,
        attributes=COMMENT_ALLOWED_ATTRIBUTES,
        protocols=COMMENT_ALLOWED_PROTOCOLS,
        strip=True,
        strip_comments=True,
    )
    return rich_content
