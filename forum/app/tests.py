import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Category, Tag, Question, Comment, Answer, Vote, View, Article, ArticleComment


class ForumTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')
        self.tag = Tag.objects.create(name='Test Tag')
        self.question = Question.objects.create(title='Test Question', content='Test Content', category=self.category,author_id=1)
        self.answer = Answer.objects.create(content='Test Answer', question=self.question,author_id=1)
        self.comment = Comment.objects.create(content='Test comment', answer=self.answer, author_id=2)

    def test_add_category(self):
        url = reverse('add_category')
        data = {'name': 'New Category'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 2)

    def test_add_tag(self):
        url = reverse('add_tag')
        data = {'name': 'New Tag'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Tag.objects.count(), 2)

    def test_add_answer(self):
        url = reverse('add_answer')
        data = {'answer': {'question': self.question.id, 'content': 'Test Answer', 'author_id': 1}}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Answer.objects.count(), 2)

    def test_add_comment(self):
        url = reverse('add_comment')
        data = {'comment': {'answer': self.answer.id, 'content': 'Test Comment', 'author_id': 2}}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 2)

    def tearDown(self):
        self.category.delete()
        self.tag.delete()
        self.question.delete()
        self.answer.delete()
        self.comment.delete()

