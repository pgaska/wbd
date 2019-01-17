from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hurtownia/', views.hurtownia, name='hurtownia'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('magazines/', views.magazines, name='magazines'),
    path('filter_magazines/', views.filter_magazines, name='filter_magazines'),
    path('add_magazine/', views.add_magazine, name='add_magazine'),
    path('post_magazine/', views.post_magazine, name='post_magazine'),
    path('magazines/magazine_details/<int:id_magazynu>/', views.magazine_details, name='magazine_details'),
    path('magazines/magazine_details/<int:id_magazynu>/delete_magazine/', views.delete_magazine, name="delete_magazine"),
    path('magazines/magazine_details/<int:id_magazynu>/update_magazine/', views.update_magazine, name="update_magazine"),
    path('workers/', views.workers, name='workers'),
    path('filter_workers/', views.filter_workers, name='filter_workers'),
    path('add_worker/', views.add_worker, name='add_worker'),
    path('post_worker/', views.post_worker, name='post_worker'),
    path('workers/worker_details/<int:id_pracownika>/', views.worker_details, name='worker_details'),
    path('workers/worker_details/<int:id_pracownika>/delete_worker/', views.delete_worker, name="delete_worker"),
    path('workers/worker_details/<int:id_pracownika>/update_worker/', views.update_worker, name="update_worker"),
    path('goods/', views.goods, name='goods'),
]