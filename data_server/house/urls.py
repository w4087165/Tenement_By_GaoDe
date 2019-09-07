"""
    url
"""
from django.conf.urls import url
from. import views


urlpatterns = [
    #http://127.0.0.1:8000/v1/houses
    url(r'^$', views.house_views),
    # url(r'^/(?P<username>[\w]{1,11})$',views.user_views),#  --可能有问题
    # url(r'^/(?P<username>[\w]{1,11})/avatar$',views.user_avatar),
]