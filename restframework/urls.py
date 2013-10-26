from django.conf import settings
from django.conf.urls import patterns, include, url, static

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',

    # admin
    url(r'^admin/', include(admin.site.urls)),

    # rest framework
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # blog
    url(r'^blog/', include('blog.urls', namespace='blog'))
)
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
