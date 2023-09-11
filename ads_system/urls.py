from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path("support/", views.support),
    path("create_ad/", views.create_ad),
    path("myads/", views.myads),
    path("ad/", views.ad_view)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
