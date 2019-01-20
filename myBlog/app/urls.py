from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from app import views

urlpatterns = [
    url(r'^$', views.index.as_view()),
    url(r'^login/$', views.adminlogin.as_view()),
    url(r'^posts$', views.Posts.as_view()),
    url(r'^postsdetail/(?P<id>[0-9]+)/$', views.PostsDetail.as_view()),
    url(r'^term/$', views.Terms.as_view()),
    url(r'^termsdetail/$', views.TermsDetail.as_view()),
    url(r'^comments/$', views.Comments.as_view()),
    url(r'^commentsdetail/$', views.CommentsDetail.as_view()),
    url(r'^links/$', views.Links.as_view()),
    url(r'^linkdetail/$', views.LinksDetail.as_view()),
    url(r'^tag/$', views.tags.as_view()),
    url(r'^archives/$', views.archives.as_view()),
    url(r'^article/$', views.article.as_view()),
    url(r'^addposts$', views.AddPosts.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)