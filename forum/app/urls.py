from django.urls import path

from . import views

urlpatterns = [
    path('add_category', views.add_category, name='add-category'),
    path('all_categories', views.all_category, name='all-catg'),
    path('add_tag', views.add_tag, name='add-tag'),
    path('all_tags', views.all_tags, name='all-tags'),
    path('add_comment', views.add_comment, name='add-comment'),
    path('add_question', views.add_question, name='add-question'),
    path('all_questions', views.all_questions, name='all-questions'),
    path('get_question/<int:id>/', views.one_question, name='one-question'),
    path('comments_question/<int:id>/', views.get_all_comments_by_question, name='comments-question'),


]
