from django.db import models
from django.urls import reverse
# Create your models here.

class Article(models.Model):
    '''Model representing a blog article.'''
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    # image = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        return f'{self.title} by {self.author}'
    
    def get_absolute_url(self):
        return reverse('article', kwargs={'pk': self.pk})
    
    def get_all_comments(self):
        return Comment.objects.filter(article=self)
    
class Comment(models.Model):
    '''Model representing a comment on an article.'''
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.text}'