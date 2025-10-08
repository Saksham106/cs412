from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
import random
from django.urls import reverse


# Create your views here.
class ShowAllView(ListView):
    model = Article
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'


class ArticleView(DetailView):
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

class RandomArticleView(DetailView):
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

    def get_object(self):
        articles = list(Article.objects.all())
        return random.choice(articles)

class CreateArticleView(CreateView):
    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

    def form_valid(self, form):
        # Save the article first
        response = super().form_valid(form)
        return response

class CreateCommentView(CreateView):
    form_class = CreateCommentForm
    template_name = 'blog/create_comment_form.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('article', kwargs={'pk': pk})
    
    def get_context_data(self):
        context = super().get_context_data()
        context['article'] = Article.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        form.instance.article = article
        return super().form_valid(form)
    
class UpdateArticleView(UpdateView):
    model = Article
    form_class = UpdateArticleForm
    template_name = 'blog/update_article_form.html'

class DeleteCommentView(DeleteView):
    model = Comment
    template_name = 'blog/delete_comment_form.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)
        article = comment.article
        return reverse('article', kwargs={'pk': article.pk})