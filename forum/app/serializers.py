
from django.db.models import fields
from rest_framework import serializers

from .models import Question, Tag, Comment, Category


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('title', 'content', 'views_number', 'created_at', 'updated_at', 'author', 'category', 'tags')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('content', 'votes', 'up_vote', 'down_vote', 'created_at', 'updated_at', 'question')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'created_at', 'updated_at')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'created_at', 'updated_at')
