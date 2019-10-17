from django import forms
from webapp.models import Article, Comment


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['created_at', 'updated_at']


class CommentForm(forms.ModelForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fields['article'].queryset = Article.objects.oll

    class Meta:
        model = Comment
        exclude = ['created_at', 'updated_at']


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")
