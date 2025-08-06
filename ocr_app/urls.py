from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    path("", views.upload_image, name="upload_image"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
