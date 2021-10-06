from django_comments.abstracts import BaseCommentAbstractModel
from django_comments.forms import CommentForm


def get_model() -> BaseCommentAbstractModel:
    from comments.models import PostComment
    return PostComment


def get_form() -> CommentForm:
    from comments.forms import PostCommentForm
    return PostCommentForm
