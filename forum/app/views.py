from django.shortcuts import render

# Create your views here.
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, Tag, Question, Comment, Answer
from .serializers import CategorySerializer, TagSerializer, CommentSerializer, QuestionSerializer, AnswerSerializer


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
def add_answer(request):
    print(request)
    answer_data = request.data.get('answer', {})
    question_id = answer_data.get('question', None)
    if question_id:
        question = Question.objects.get(pk=question_id)
        answer_data['question'] = question.id

    answer = AnswerSerializer(data=answer_data)
    if answer.is_valid():
        answer.save()
        return Response(answer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(answer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        author_id=question_data.get('author_id', None),
        author_name=question_data.get('author_name', None),
        author_image=question_data.get('author_image', None),
        title=question_data.get('title', ""),
        content=question_data.get('content', ""),
        category=category,
    )
    question.save()
    question.tags.set(question_tags)

    question_serializer = QuestionSerializer(question)
    return Response(question_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def update_question(request):
    question_data = request.data.get('question', {})
    print(question_data)
    question_id=question_data.get('id', None)
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

    # Mettre à jour les champs de la question à partir des données de la requête

    question.title = question_data.get('title', question.title)
    question.content = question_data.get('content', question.content)
    question.category_id = question_data.get('category_id', question.category_id)

    # Mettre à jour les tags de la question
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
    question.tags.set(question_tags)

    question.save()

    question_serializer = QuestionSerializer(question)
    return Response(question_serializer.data)


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
        return  Response([])


@api_view(['GET'])
def all_questions(request):
    questions = Question.objects.all().order_by('-created_at')
    if questions:
        serializer = QuestionSerializer(questions, many=True)
        data = serializer.data
        for question in data:
            answers_count = Answer.objects.filter(question_id=question['id']).count()
            question['answers_count'] = answers_count
        return Response(data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def questions_by_user(request,id):
    questions = Question.objects.filter(author_id=id).order_by('-created_at')
    if questions:
        serializer = QuestionSerializer(questions, many=True)
        data = serializer.data
        for question in data:
            answers_count = Answer.objects.filter(question_id=question['id']).count()
            question['answers_count'] = answers_count
        return Response(data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def answers_by_user(request,id):
    answers = Answer.objects.filter(author_id=id).order_by('-created_at')
    if answers:
        serializer = AnswerSerializer(answers, many=True)
        data = serializer.data
        for answer in data:
            comments_count = Comment.objects.filter(answer_id=answer['id']).count()
            answer['comments_count'] = comments_count
        return Response(data)
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
def get_all_answers_by_question(request, id):
    answers = Answer.objects.filter(question_id=id).prefetch_related('comment_set')
    if answers:
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def add_comment(request):
    comment_data = request.data.get('comment', {})
    answer_id = comment_data.get('answer', None)
    if answer_id:
        answer = Answer.objects.get(pk=answer_id)
        comment_data['answer'] = answer.id

    comment = CommentSerializer(data=comment_data)
    if comment.is_valid():
        comment.save()
        return Response(comment.data, status=status.HTTP_201_CREATED)
    else:
        return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_question_with_answers_and_comments(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    answers = Answer.objects.filter(question=question_id)

    serialized_answers = []
    for answer in answers:
        comments = Comment.objects.filter(answer=answer)
        serialized_comments = CommentSerializer(comments, many=True).data
        serialized_answer = AnswerSerializer(answer).data
        serialized_answer['comments'] = serialized_comments
        serialized_answers.append(serialized_answer)

    serialized_question = QuestionSerializer(question).data
    serialized_question['answers'] = serialized_answers

    return Response(serialized_question, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_answer_vote(request,id):
    try:
        answer = Answer.objects.get(pk=id)
    except Answer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    vote = request.data.get('vote', "")

    if vote == 'up':
        print(vote)
        answer.votes += 1
        answer.up_vote += 1

    elif vote == 'down':
        answer.votes -= 1
        answer.down_vote += 1
    else :
        return Response(status=status.HTTP_400_BAD_REQUEST)
    answer.save()
    serialized_answer = AnswerSerializer(answer).data

    return Response(serialized_answer, status=status.HTTP_200_OK)


@api_view(['GET'])
def solution_answer_question(request, id):
    try:
        answer = Answer.objects.get(pk=id)
    except Answer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    answer.solution=True
    answer.save()
    serialized_answer = AnswerSerializer(answer).data

    return Response(serialized_answer, status=status.HTTP_200_OK)

