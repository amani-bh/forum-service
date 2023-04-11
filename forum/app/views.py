from django.shortcuts import render

# Create your views here.
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, Tag
from .serializers import CategorySerializer, TagSerializer, CommentSerializer, QuestionSerializer


@api_view(['POST'])
def add_category(request):
    catg = CategorySerializer(data=request.data)

    if Category.objects.filter(name=request.data['name']).exists():
        return Response({'error': 'This category already exists'})

    if catg.is_valid():
        catg.save()
        return Response(catg.data, status=status.HTTP_201_CREATED)
    else:
        return Response(catg.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_tag(request):
    tag = TagSerializer(data=request.data)

    if Tag.objects.filter(name=request.data['name']).exists():
        return Response({'error': 'This tag already exists'})

    if tag.is_valid():
        tag.save()
        return Response(tag.data, status=status.HTTP_201_CREATED)
    else:
        return Response(tag.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_comment(request):
    comment = CommentSerializer(data=request.data)
    if comment.is_valid():
        comment.save()
        return Response(comment.data, status=status.HTTP_201_CREATED)
    else:
        return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_question(request):
    question = QuestionSerializer(data=request.data)
    if question.is_valid():
        question.save()
        return Response(question.data, status=status.HTTP_201_CREATED)
    else:
        return Response(question.errors, status=status.HTTP_400_BAD_REQUEST)

