from django.conf.urls import patterns, url, include

from rest_framework import routers

from .views import ArticleViewSet, CategoryViewSet, TagViewSet
from .views import article_list, article_detail, article_list_rest, article_detail_rest
from .views import ArticleList, ArticleDetail
from .views import ArticleListMixin, ArticleDetailMixins
from .views import ArticleListGeneric, ArticleDetailGeneric
from .views import api_root
from .views import play_with_serializers, play_model_serializers

router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)


urlpatterns = patterns(
    '',

    # api root
    url(r'^$', api_root, name='api-root'),

    # viewsets.ModelViewSet
    url(r'^routers/', include(router.urls)),

    # low level views
    url(r'^low-view/articles/$', article_list, name='low-articles-list'),
    url(r'^low-view/articles/(?P<pk>\d+)/$', article_detail),

    # function based views
    url(r'^func-view/articles/$', article_list_rest, name='func-articles-list'),
    url(r'^func-view/articles/(?P<pk>\d+)/$', article_detail_rest),

    # class based views
    url(r'^class-view/articles/$', ArticleList.as_view(), name='class-articles-list'),
    url(r'^class-view/articles/(?P<pk>\d+)/$', ArticleDetail.as_view()),

    # mixins
    url(r'^mixins-view/articles/$', ArticleListMixin.as_view(), name='mixins-articles-list'),
    url(r'^mixins-view/articles/(?P<pk>\d+)/$', ArticleDetailMixins.as_view()),

    # generic
    url(r'^generic-view/articles/$', ArticleListGeneric.as_view(), name='generic-articles-list'),
    url(r'^generic-view/articles/(?P<pk>\d+)/$', ArticleDetailGeneric.as_view()),

    # play with serializers
    url(r'^serializers/$', play_with_serializers),
    url(r'^serializers/model/$', play_model_serializers),
)