from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns=[
        url('^$', views.index, name = 'index'),
        url(r'^home$', views.home, name = 'home'),
        url(r'^upload_image/$', views.image, name = 'image'),
        url(r'^accounts/profile/$', views.profile, name = 'profile'),
        url(r'^profile/(\d+)/$', views.otherprofile, name = 'otherprofile'),
        url(r"^search/",views.search,name="search"),
        url(r'^profile/update/$',views.update,name='update'),
        url(r'^comment/(\d+)/$',views.comment,name='comment'),
        url(r'^like/(\d+)/$',views.like,name='like'),
        url(r'^follow/(\d+)/$',views.follow,name='follow'),
    ]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)