from django.urls import path

from . import views

urlpatterns = [
    path('add_category', views.add_category, name='add-category'),
    path('add_tag', views.add_tag, name='add-tag'),
    path('add_comment', views.add_tag, name='add-comment'),
    path('add_question', views.add_tag, name='add-question'),


]
