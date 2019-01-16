from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hurtownia/', views.hurtownia, name='hurtownia'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('magazines/', views.magazines, name='magazines'),
    path('workers/', views.workers, name='workers'),
    path('goods/', views.goods, name='goods'),
    path('filter_magazines/', views.filter_magazines, name='filter_magazines'),
    path('add_magazine/', views.add_magazine, name='add_magazine'),
    path('post_magazine/', views.post_magazine, name='post_magazine'),
    path('magazines/magazine_details/<int:id_magazynu>/', views.magazine_details, name='magazine_details'),
    path('magazines/magazine_details/<int:id_magazynu>/delete_magazine/', views.delete_magazine, name="delete_magazine"),
    path('magazines/magazine_details/<int:id_magazynu>/update_magazine/', views.update_magazine, name="update_magazine"),
]