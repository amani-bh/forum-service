from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category, Tag, Question, Comment, Answer, Vote, View, Article, ArticleComment
from .serializers import CategorySerializer, TagSerializer, CommentSerializer, QuestionSerializer, AnswerSerializer, \
    VoteSerializer, ViewSerializer, ArticleSerializer, ArticleCommentSerializer


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
def update_answer_vote(request,id,idUser):
    try:
        vote_user=Vote.objects.get(user_id=idUser,answer=id)
        return Response("user already voted",status=status.HTTP_400_BAD_REQUEST)
    except Vote.DoesNotExist:
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
        voteT = VoteSerializer(data={"answer":id,"user_id":idUser})
        if voteT.is_valid():
            voteT.save()
            return Response(serialized_answer, status=status.HTTP_201_CREATED)
        else:
            return Response(voteT.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(['GET'])
def answer_by_id(request,id):
   try:
        answer = Answer.objects.get(pk=id)
        return Response(AnswerSerializer(answer).data, status=status.HTTP_200_OK)

   except Answer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_answer(request,id):
    try:
        answer = Answer.objects.get(pk=id)
    except Answer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    content = request.data.get('content', "")
    answer.content=content
    answer.save()
    serialized_answer = AnswerSerializer(answer).data
    return Response(serialized_answer, status=status.HTTP_200_OK)


@api_view(['GET'])
def search_question (request):
    query = request.GET.get('query', '')
    print(query)
    if query:
        questions = Question.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    else:
        questions = Question.objects.all().order_by('-created_at')

    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def add_view_question(request,id,idUser):
    try:
        view_user=View.objects.get(user_id=idUser,question=id)
        return Response("view exist",status=status.HTTP_400_BAD_REQUEST)
    except View.DoesNotExist:
        view = ViewSerializer(data={"user_id":idUser,"question":id})
        if view.is_valid():
            try:
                question = Question.objects.get(pk=id)
            except Question.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            view.save()
            question.views_number+=1
            question.save()
            return Response(view.data, status=status.HTTP_201_CREATED)
        else:
            return Response(view.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def delete_answer(request,id):
    try:
        answer = Answer.objects.get(pk=id)
    except Answer.DoesNotExist:
        return Response( status=status.HTTP_404_NOT_FOUND)
    answer.delete()
    return Response({"message": "deleted"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_comment(request,id):
    try:
        comment = Comment.objects.get(pk=id)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    content = request.data.get('content', "")
    comment.content=content
    comment.save()
    serialized_coment = CommentSerializer(comment).data
    return Response(serialized_coment, status=status.HTTP_200_OK)


@api_view(['GET'])
def comment_by_id(request,id):

   try:
        comment = Comment.objects.get(pk=id)
        return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)

   except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def delete_comment(request,id):
    try:
        comment = Comment.objects.get(pk=id)
    except Comment.DoesNotExist:
        return Response( status=status.HTTP_404_NOT_FOUND)
    comment.delete()
    return Response({"message": "deleted"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def delete_question(request,id):
    try:
        question = Question.objects.get(pk=id)
    except Question.DoesNotExist:
        return Response( status=status.HTTP_404_NOT_FOUND)
    question.delete()
    return Response({"message": "deleted"}, status=status.HTTP_200_OK)




@api_view(['POST'])
def add_article(request):
    article_data = request.data.get('article', {})
    tags = article_data.get('tags', [])
    article_tags = []
    if len(tags) != 0:
        for tag in tags:
            tag_serializer = TagSerializer(data={"name": tag['text']})
            if not Tag.objects.filter(name=tag['text']).exists():
                if tag_serializer.is_valid():
                    saved_tag = tag_serializer.save()
                    article_tags.append(saved_tag)
            else:
                existing_tag = Tag.objects.filter(name=tag['text']).first()
                article_tags.append(existing_tag)

    article = Article(
        author_id=article_data.get('author_id', None),
        author_name=article_data.get('author_name', None),
        author_image=article_data.get('author_image', None),
        author_badge=article_data.get('author_badge', None),
        title=article_data.get('title', ""),
        content=article_data.get('content', "")
    )
    article.save()
    article.tags.set(article_tags)
    articleserializer = ArticleSerializer(article)
    return Response(articleserializer.data, status=status.HTTP_201_CREATED)




@api_view(['GET'])
def article_by_id(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    comments = ArticleComment.objects.filter(article=article_id)

    serialized_comments = []
    for comment in comments:
        serialized_comment = ArticleCommentSerializer(comment).data
        serialized_comments.append(serialized_comment)

    serialized_article = ArticleSerializer(article).data
    serialized_article['comments'] = serialized_comments

    return Response(serialized_article, status=status.HTTP_200_OK)



@api_view(['GET'])
def all_articles(request):
    articles = Article.objects.all().order_by('-created_at')
    if articles:
        serializer = ArticleSerializer(articles, many=True)
        data = serializer.data
        for article in data:
            comments_count = ArticleComment.objects.filter(article_id=article['id']).count()
            article['comments_count'] = comments_count
        return Response(data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def add_comment_article(request):
    comment_data = request.data.get('comment', {})
    article_id = comment_data.get('article', None)
    if article_id:
        article = Article.objects.get(pk=article_id)
        comment_data['article'] = article.id

    comment = ArticleCommentSerializer(data=comment_data)
    if comment.is_valid():
        comment.save()
        return Response(comment.data, status=status.HTTP_201_CREATED)
    else:
        return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def one_article(request,id):
    article = Article.objects.filter(pk=id).first()
    if article:
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_article(request):
    article_data = request.data.get('article', {})
    article_id=article_data.get('id', None)
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        return Response({"error": "Article not found"}, status=status.HTTP_404_NOT_FOUND)

    # Mettre à jour les champs de l'article à partir des données de la requête

    article.title = article_data.get('title', article.title)
    article.content = article_data.get('content', article.content)

    # Mettre à jour les tags de l'article'
    tags = article_data.get('tags', [])
    article_tags = []
    if len(tags) != 0:
        for tag in tags:
            tag_serializer = TagSerializer(data={"name": tag['text']})
            if not Tag.objects.filter(name=tag['text']).exists():
                if tag_serializer.is_valid():
                    saved_tag = tag_serializer.save()
                    article_tags.append(saved_tag)
            else:
                existing_tag = Tag.objects.filter(name=tag['text']).first()
                article_tags.append(existing_tag)
    article.tags.set(article_tags)

    article.save()

    article_serializer = ArticleSerializer(article)
    return Response(article_serializer.data)



@api_view(['GET'])
def delete_article(request,id):
    try:
        article = Article.objects.get(pk=id)
    except Article.DoesNotExist:
        return Response( status=status.HTTP_404_NOT_FOUND)
    article.delete()
    return Response({"message": "deleted"}, status=status.HTTP_200_OK)
