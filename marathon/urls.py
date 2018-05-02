from django.conf.urls import url
from . import views
urlpatterns = [
  url(
    r'^ajax/count/$',
    views.unread_count,
    name='ajax_unread_counter',
    ),
]