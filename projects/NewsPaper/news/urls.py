
from .views import news, detail, PostList, PostDetail, news_home
from django.urls import path




urlpatterns = [
    path('news_list/', news, name='news'),
    path('', news_home, name='news_home'),
    path('news_list/<str:slug>', detail, name='detail'),

]