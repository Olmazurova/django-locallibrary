from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book_detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author_detail'),
    # re_path(r'^/url/$', views.my_reused_view, {'my_template_name': 'some_path'}, name='aurl'),
    # re_path(r'^/anotherurl/$', views.my_reused_view, {'my_template_name': 'another_path'}, name='anotherurl'),
]
