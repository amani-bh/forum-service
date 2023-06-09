from django.urls import path

from . import views

urlpatterns = [
    path('add_category', views.add_category, name='add_category'),
    path('all_categories', views.all_category, name='all-catg'),
    path('add_tag', views.add_tag, name='add_tag'),
    path('all_tags', views.all_tags, name='all-tags'),
    path('add_answer', views.add_answer, name='add_answer'),
    path('update_question', views.update_question, name='update_question'),
    path('add_question', views.add_question, name='add_question'),
    path('all_questions', views.all_questions, name='all-questions'),
    path('get_question/<int:id>/', views.one_question, name='one-question'),
    path('answers_question/<int:id>/', views.get_all_answers_by_question, name='answers-question'),
    path('solution_answer_question/<int:id>/', views.solution_answer_question, name='solution_answer_question'),
    path('add_comment', views.add_comment, name='add_comment'),
    path('question/<int:question_id>/', views.get_question_with_answers_and_comments, name='get_question_with_answers_and_comments'),
    path('update_answer_vote/<int:id>/<int:idUser>', views.update_answer_vote, name='add-update_answer_vote'),
    path('question_by_user/<int:id>/', views.questions_by_user, name='question_by_user'),
    path('answers_by_user/<int:id>/', views.answers_by_user),
    path('answer_by_id/<int:id>/', views.answer_by_id),
    path('update_answer/<int:id>', views.update_answer),
    path('search_question', views.search_question),
    path('add_view_question/<int:id>/<int:idUser>', views.add_view_question),
    path('delete_answer/<int:id>', views.delete_answer),
    path('update_comment/<int:id>', views.update_comment),
    path('comment_by_id/<int:id>/', views.comment_by_id),
    path('delete_comment/<int:id>', views.delete_comment),
    path('delete_question/<int:id>', views.delete_question),
    path('add_article', views.add_article),
    path('all_articles', views.all_articles),
    path('article_by_id/<int:article_id>', views.article_by_id),
    path('add_comment_article', views.add_comment_article),
    path('get_article/<int:id>/', views.one_article),
    path('update_article', views.update_article),
    path('delete_article/<int:id>', views.delete_article),



]
