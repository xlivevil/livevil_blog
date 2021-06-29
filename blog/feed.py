from django.contrib.syndication.views import Feed

from blog.models import Post


class AllPostsRssFeed(Feed):
    """
    Rss设置
    """
    # 标题
    title = "Xlivevil"
    # 网址
    link = "/"
    # 描述信息
    description = "Xlivevil 的全部文章"

    # 显示内容
    def items(self):
        return Post.objects.all()

    # 内容条目的标题
    def item_title(self, item):
        return "[%s] %s" % (item.category, item.title)

    # 描述
    def item_description(self, item):
        return item.body_html
