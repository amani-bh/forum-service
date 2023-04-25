from django.urls import path

from . import views

urlpatterns = [
    path('add_category', views.add_category, name='add-category'),
    path('all_categories', views.all_category, name='all-catg'),
    path('add_tag', views.add_tag, name='add-tag'),
    path('all_tags', views.all_tags, name='all-tags'),
    path('add_answer', views.add_answer, name='add-answer'),
    path('add_question', views.add_question, name='add-question'),
    path('all_questions', views.all_questions, name='all-questions'),
    path('get_question/<int:id>/', views.one_question, name='one-question'),
    path('answers_question/<int:id>/', views.get_all_answers_by_question, name='answers-question'),
    path('solution_answer_question/<int:id>/', views.get_solution_answer_question, name='solution_answer_question'),
    path('add_comment', views.add_comment, name='add-comment'),
    path('question/<int:question_id>/', views.get_question_with_answers_and_comments, name='get_question_with_answers_and_comments'),


]