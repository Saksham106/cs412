from django.db import models

# Create your models here.

class Article(models.Model):
    '''Model representing a blog article.'''
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    image = models.URLField(blank=True)

    def __str__(self):
        return f'{self.title} by {self.author}'