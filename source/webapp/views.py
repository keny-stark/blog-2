from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import ArticleForm, CommentForm
from webapp.models import Article, Comment


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.all()
        return context


class ArticleView(TemplateView):
    template_name = 'article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_pk = kwargs.get('pk')
        context['article'] = get_object_or_404(Article, pk=article_pk)
        return context


class ArticleCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, 'create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article = Article.objects.create(
                title=form.cleaned_data['title'],
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text'],
                category=form.cleaned_data['category']
            )
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'create.html', context={'form': form})


class ArticleUpdateView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        form = ArticleForm(data={
            'title': article.title,
            'author': article.author,
            'text': article.text,
            'category': article.category_id
        })
        return render(request, 'update.html', context={'form': form, 'article': article})

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.author = form.cleaned_data['author']
            article.text = form.cleaned_data['text']
            article.category = form.cleaned_data['category']
            article.save()
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'update.html', context={'form': form, 'article': article})


class ArticleDeleteView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        return render(request, 'delete.html', context={'article': article})

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        article.delete()
        return redirect('index')


class CommentCreateView(View):
    def get(self, request, *args, **kwargs):
        form = CommentForm()
        return render(request, 'comment/create.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = Comment.objects.create(
                author=form.cleaned_data['author'],
                text=form.cleaned_data['text'],
                article=form.cleaned_data['article']
            )
            # это нужно исправить на ваш url.
            return redirect('article_view', pk=comment.article.pk)
        else:
            return render(request, 'comment/create.html', context={'form': form})


class CommentsView(TemplateView):
    template_name = 'comment/comments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.order_by('-created_at')
        return context


class CommentUpdateView(View):
    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get('pk'))
        form = ArticleForm(data={
            'author': comment.author,
            'text': comment.text,
        })
        return render(request, 'comment/update_comment.html', context={'form': form, 'comment': comment})

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Article, pk=kwargs.get('pk'))
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            comment.author = form.cleaned_data['author']
            comment.text = form.cleaned_data['text']
            comment.save()
            return redirect('comment_view')
        else:
            return render(request, 'update.html', context={'form': form, 'comment': comment})


class CommentDeleteView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        return render(request, 'delete.html', context={'article': article})

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        article.delete()
        return redirect('index')