from django.shortcuts import render

# Create your views here.
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, Tag, Question, Comment
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
    comment_data = request.data.get('comment', {})
    question_id = comment_data.get('question', None)
    if question_id:
        question = Question.objects.get(pk=question_id)
        comment_data['question'] = question.id

    print (comment_data)
    comment = CommentSerializer(data=comment_data)
    if comment.is_valid():
        comment.save()
        return Response(comment.data, status=status.HTTP_201_CREATED)
    else:
        return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_question(request):
    question_data = request.data.get('question', {})
    tags = question_data.get('tags', [])
    question_tags = []
    if len(tags) != 0:
        for tag in tags:
            tag_serializer = TagSerializer(data={"name": tag['text']})
            if not Tag.objects.filter(name=tag['text']).exists():
                if tag_serializer.is_valid():
                    saved_tag = tag_serializer.save()
                    question_tags.append(saved_tag)
            else:
                existing_tag = Tag.objects.filter(name=tag['text']).first()
                question_tags.append(existing_tag)

    try:
        category_id = question_data.get('category_id', None)
        category = Category.objects.filter(pk=category_id).first()
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

    question = Question(
        author=1,
        title=question_data.get('title', ""),
        content=question_data.get('content', ""),
        category=category,
    )
    question.save()
    question.tags.set(question_tags)

    question_serializer = QuestionSerializer(question)
    return Response(question_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def all_category(request):
    categories = Category.objects.all()
    if categories:
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def all_tags(request):
    tags = Tag.objects.all()
    if tags:
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def all_questions(request):
    questions = Question.objects.all().order_by('-created_at')
    if questions:
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def one_question(request,id):
    question = Question.objects.filter(pk=id).first()
    if question:
        serializer = QuestionSerializer(question)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_all_comments_by_question(request,id):
    comments = Comment.objects.filter(question_id=id)
    if comments:
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
