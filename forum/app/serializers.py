
from django.db.models import fields
from rest_framework import serializers

from .models import Question, Tag, Comment, Category


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'created_at', 'updated_at')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', "name", 'created_at', 'updated_at')


class QuestionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    category = CategorySerializer( read_only=True)

    class Meta:
        model = Question
        fields = '__all__'
        depth = 1


class CommentSerializer(serializers.ModelSerializer):
    #question = QuestionSerializer( read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'





