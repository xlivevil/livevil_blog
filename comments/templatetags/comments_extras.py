from django import template
from django_comments.templatetags.comments import RenderCommentFormNode

import comments

register = template.Library()


class RenderMPTTCommentFormNode(RenderCommentFormNode):
    def get_form(self, context):
        obj = self.get_object(context)
        user = context['request'].user
        if obj:
            return comments.get_form()(obj, user=user)
        else:
            return None


@register.tag
def render_post_comment_form(parser, token):
    return RenderMPTTCommentFormNode.handle_token(parser, token)
# TODO: 更改跳转posted页面为至本页刷新并msg
