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
    path('magazines/magazine_details/<int:id_magazynu>/magazine_goods/', views.magazine_goods, name="magazine_goods"),
    path('magazines/magazine_details/<int:id_magazynu>/filter_magazine_goods/', views.filter_magazine_goods, name="filter_magazine_goods"),
    path('workers/', views.workers, name='workers'),
    path('filter_workers/', views.filter_workers, name='filter_workers'),
    path('add_worker/', views.add_worker, name='add_worker'),
    path('post_worker/', views.post_worker, name='post_worker'),
    path('workers/worker_details/<int:id_pracownika>/', views.worker_details, name='worker_details'),
    path('workers/worker_details/<int:id_pracownika>/delete_worker/', views.delete_worker, name="delete_worker"),
    path('workers/worker_details/<int:id_pracownika>/update_worker/', views.update_worker, name="update_worker"),
    path('goods/', views.goods, name='goods'),
    path('filter_goods/', views.filter_goods, name='filter_goods'),
    path('add_goods/', views.add_goods, name='add_goods'),
    path('choose_type/', views.choose_type, name='choose_type'),
    path('add_procesor/', views.add_procesor, name='add_procesor'),
    path('add_pamiec/', views.add_pamiec, name='add_pamiec'),
    path('add_karta_graficzna/', views.add_karta_graficzna, name='add_karta_graficzna'),
    path('add_plyta_glowna/', views.add_plyta_glowna, name='add_plyta_glowna'),
    path('post_procesor/', views.post_procesor, name='post_procesor'),
    path('post_pamiec/', views.post_pamiec, name='post_pamiec'),
    path('post_plyta_glowna/', views.post_plyta_glowna, name='post_plyta_glowna'),
    path('post_karta_graficzna/', views.post_karta_graficzna, name='post_karta_graficzna'),
    path('goods/goods_details/<int:id_towaru>/', views.goods_details, name='goods_details'),
    path('goods/goods_details/<int:id_towaru>/delete_goods/', views.delete_goods, name="delete_goods"),
    path('goods/goods_details/<int:id_towaru>/update_goods/', views.update_goods, name="update_goods"),
    path('workers/worker_details/<int:id_pracownika>/salaries', views.salaries, name='salaries'),
    path('workers/worker_details/<int:id_pracownika>/post_salary', views.post_salary, name='post_salary'),
]