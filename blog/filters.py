import django_filters

from .models import Article


class ArticleFilter(django_filters.FilterSet):
    min_id = django_filters.NumberFilter(lookup_type='gte', name='id')
    # max_id = django_filters.NumberFilter(lookup_type='lte')

    class Meta:
        model = Article
        fields = ['category', 'title', 'min_id']