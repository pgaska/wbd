from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hurtownia/', views.hurtownia, name='hurtownia'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('magazines/', views.magazines, name='magazines'),
    path('workers/', views.workers, name='workers'),
    path('goods/', views.goods, name='goods')
]