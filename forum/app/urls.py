from django.urls import path

from . import views

urlpatterns = [
    path('add_category', views.add_category, name='add-category'),
    path('all_categories', views.all_category, name='all-catg'),
    path('add_tag', views.add_tag, name='add-tag'),
    path('all_tags', views.all_tags, name='all-tags'),
    path('add_answer', views.add_answer, name='add-answer'),
    path('update_question', views.update_question, name='update_question'),
    path('add_question', views.add_question, name='add-question'),
    path('all_questions', views.all_questions, name='all-questions'),
    path('get_question/<int:id>/', views.one_question, name='one-question'),
    path('answers_question/<int:id>/', views.get_all_answers_by_question, name='answers-question'),
    path('solution_answer_question/<int:id>/', views.solution_answer_question, name='solution_answer_question'),
    path('add_comment', views.add_comment, name='add-comment'),
    path('question/<int:question_id>/', views.get_question_with_answers_and_comments, name='get_question_with_answers_and_comments'),
    path('update_answer_vote/<int:id>/<int:idUser>', views.update_answer_vote, name='add-update_answer_vote'),
    path('question_by_user/<int:id>/', views.questions_by_user, name='question_by_user'),
    path('answers_by_user/<int:id>/', views.answers_by_user),
    path('answer_by_id/<int:id>/', views.answer_by_id),
    path('update_answer/<int:id>', views.update_answer),
    path('search_question', views.search_question),
    path('add_view_question/<int:id>/<int:idUser>', views.add_view_question),
    path('delete_answer/<int:id>', views.delete_answer),


]
