from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    #API paths
    path('edit_post/<int:id>', views.edit_post, name="edit_post"),
    path('update_task/<str:ids>', views.update_task, name="update_task"),
    path('remove/<str:ids>', views.remove_task, name="update_task"),
    path('edit_task_name/<int:task_id>/<int:entry_id>/<str:new_task_name>', views.edit_task_name, name="edit_task_name"),
    path('add_task/<int:entry_id>/<str:task_name>', views.add_task, name="add_task"),
    path('compose/<str:main_id>/<str:entry_date>/<str:body>', views.compose, name='compose'),
    path('delete_entry/<int:entry_id>', views.delete_entry, name="delete_entry"),


]