from django_filters import rest_framework as drf_filters

from blog.models import Post


class PostFilter(drf_filters.FilterSet):
    # TODO: 修改完善
    created_year = drf_filters.NumberFilter(field_name='create_time',
                                            lookup_expr='year',
                                            help_text='年份')
    created_month = drf_filters.NumberFilter(field_name='create_time',
                                             lookup_expr='month')
    create_daterange = drf_filters.DateRangeFilter(field_name='create_time')
    create = drf_filters.DateFilter(field_name='create_time')

    class Meta:
        model = Post
        fields = [
            'category', 'tags', 'create_daterange', 'create', 'created_year',
            'created_month'
        ]
