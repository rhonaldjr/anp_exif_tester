from django.conf.urls import url, include

app_name = 'imglibrary'

from . import views

urlpatterns = [
    url(r"^view-image/(?P<pk>\d+)$", views.ViewImage.as_view(), name="view-image"),#Upload images and then add to selected album or create new one
]
