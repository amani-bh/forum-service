from django.core.validators import MaxValueValidator
from django.db import models


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    author_id = models.PositiveIntegerField()
    author_name = models.CharField(max_length=255)
    author_image = models.URLField()
    author_badge = models.CharField(max_length=255, default="Novice")
    title = models.CharField(max_length=255)
    content = models.TextField()
    views_number = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    solved = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class Answer(models.Model):
    content = models.TextField()
    votes = models.IntegerField(default=0)
    up_vote = models.PositiveIntegerField(default=0)
    down_vote = models.IntegerField(default=0, validators=[MaxValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author_id = models.PositiveIntegerField()
    author_name = models.CharField(max_length=255,null=True)
    author_badge = models.CharField(max_length=255, default="Novice")
    author_image = models.URLField(blank=True,null=True)
    solution = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.content


class Comment(models.Model):
    content = models.TextField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    author_id = models.PositiveIntegerField()
    author_name = models.CharField(max_length=255,null=True)
    author_badge = models.CharField(max_length=255, default="Novice")
    author_image = models.URLField(null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.content


class Like(models.Model):
    user_id = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Vote(models.Model):
    user_id = models.IntegerField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class View(models.Model):
    user_id = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Article(models.Model):
    author_id = models.PositiveIntegerField()
    author_name = models.CharField(max_length=255,null=True)
    author_image = models.URLField(null=True)
    author_badge = models.CharField(max_length=255, default="Novice")
    title = models.CharField(max_length=255)
    content = models.TextField()
    views_number = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class ArticleComment(models.Model):
    content = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author_id = models.PositiveIntegerField()
    author_name = models.CharField(max_length=255,null=True)
    author_badge = models.CharField(max_length=255, default="Novice")
    author_image = models.URLField(null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.content
