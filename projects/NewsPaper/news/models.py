import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
import datetime


# Create your models here.
class Author ( models.Model ):  # Имя таблицы
    authorUser = models.OneToOneField ( User, on_delete=models.CASCADE )
    ratingAuthor = models.SmallIntegerField ( default=0 )

    def update_rating(self):
        postRat = self.post_set.all ().aggregate ( postRating=Sum ( 'rating' ) )
        pRat = 0
        pRat += postRat.get ( 'postRating' )

        commentRat = self.authorUser.comment_set.all ().aggregate ( commentRating=Sum ( 'rating' ) )
        cRat = 0
        cRat += commentRat.get ( 'commentRating' )

        self.ratingAuthor = pRat * 3 + cRat


class Category ( models.Model ):
    name = models.CharField ( max_length=64, unique=True )


class Post ( models.Model ):
    author = models.ForeignKey ( Author, on_delete=models.CASCADE )
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'НОВОСТЬ'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField ( max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE )
    dateCreation = models.DateTimeField ( auto_now_add=True )
    postCategory = models.ManyToManyField ( Category, through='PostCategory' )
    title = models.CharField ( max_length=128, unique=True )
    text = models.TextField ()
    img = models.ImageField ( upload_to='pics', blank=True )
    rating = models.SmallIntegerField ( default=0 )
    slug = models.SlugField ( max_length=80, unique=True, null=True, db_index=True, verbose_name="URL" )

    def get_absolute_url(self):
        return reverse ( 'detail', kwargs={'slug': self.slug} )

    def __str__(self):
        return format(self.title)

    def like(self):
        self.rating += 1
        self.save ()

    def dislike(self):
        self.rating -= 1
        self.save ()

    def preview(self):
        return self.text[0:123] + '...'


class PostCategory ( models.Model ):
    postThrough = models.ForeignKey ( Post, on_delete=models.CASCADE )
    categoryThrough = models.ForeignKey ( Category, on_delete=models.CASCADE )


class Comment ( models.Model ):
    commentPost = models.ForeignKey ( Post, on_delete=models.CASCADE )
    commentUser = models.ForeignKey ( User, on_delete=models.CASCADE )
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True )
    rating = models.SmallIntegerField(default=0 )


    def __str__(self):
        return self.commentUser.username

    def like(self):
        self.rating += 1
        self.save ()

    def dislike(self):
        self.rating -= 1
        self.save ()
