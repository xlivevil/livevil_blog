from django_filters import rest_framework as drf_filters

from blog.models import Post
from comments.models import PostComment


class PostFilter(drf_filters.FilterSet):

    created_year = drf_filters.NumberFilter(field_name='create_time', lookup_expr='year', help_text='年份')
    created_month = drf_filters.NumberFilter(field_name='create_time', lookup_expr='month', help_text='月份')
    create_daterange = drf_filters.DateRangeFilter(field_name='create_time')
    start_date = drf_filters.DateFilter(field_name='create_time', lookup_expr='gte')
    end_date = drf_filters.DateFilter(field_name='create_time', lookup_expr='lte')

    class Meta:
        model = Post
        fields = ['category', 'tags', 'create_daterange', 'start_date', 'end_date', 'created_year', 'created_month']


class CommentFilter(drf_filters.FilterSet):

    created_year = drf_filters.NumberFilter(field_name='submit_date', lookup_expr='year', help_text='年份')
    created_month = drf_filters.NumberFilter(field_name='submit_date', lookup_expr='month', help_text='月份')
    create_daterange = drf_filters.DateRangeFilter(field_name='submit_date')
    start_date = drf_filters.DateFilter(field_name='submit_date', lookup_expr='gte')
    end_date = drf_filters.DateFilter(field_name='submit_date', lookup_expr='lte')

    class Meta:
        model = PostComment
        fields = ['create_daterange', 'start_date', 'end_date', 'created_year', 'created_month']
