# mysite/urls.py

from django.conf.urls import url

from . import views

app_name = 'mysite'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^posts/$', views.PostsView.as_view(), name='posts'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^detail/(?P<id>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^detail/(?P<id>[0-9]+)/comment$', views.detail_comment, name='detail_comment'),
    url(r'^news$', views.news, name='news'),
    url(r'^add$',views.AddPostView.as_view(),name='add')
]
