from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path("support/", views.support),
    path("create_ad/", views.create_ad),
    path("myads/", views.myads),
    path("delete-ad/", views.delete_ad),
    path("edit-ad/", views.edit_ad),
    path("ad/", views.ad_view),
    path("categories/", views.categories),
    path("search/", views.search)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
