from rest_framework_extensions.key_constructor.bits import (
    ListSqlQueryKeyBit,
    PaginationKeyBit,
    RetrieveSqlQueryKeyBit,
)
from rest_framework_extensions.key_constructor.constructors import DefaultKeyConstructor
from .utils import UpdatedAtKeyBit


class PostUpdatedAtKeyBit(UpdatedAtKeyBit):
    key = "post_updated_at"


class PostListKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    pagination = PaginationKeyBit()
    updated_at = PostUpdatedAtKeyBit()


class PostObjectKeyConstructor(DefaultKeyConstructor):
    retrieve_sql = RetrieveSqlQueryKeyBit()
    updated_at = PostUpdatedAtKeyBit()


class CommentUpdatedAtKeyBit(UpdatedAtKeyBit):
    key = "comment_updated_at"


class CommentListKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    pagination = PaginationKeyBit()
    updated_at = CommentUpdatedAtKeyBit()


class TagUpdatedAtKeyBit(UpdatedAtKeyBit):
    key = "tag_updated_at"


class TagKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    pagination = PaginationKeyBit()
    updated_at = TagUpdatedAtKeyBit()


class CategoryUpdatedAtKeyBit(UpdatedAtKeyBit):
    key = "category_updated_at"


class CategoryKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    updated_at = CategoryUpdatedAtKeyBit()