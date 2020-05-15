def get_model():
    from comments.models import PostComment
    return PostComment


def get_form():
    from comments.forms import PostCommentForm
    return PostCommentForm
