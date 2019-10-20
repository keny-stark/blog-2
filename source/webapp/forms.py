from django import forms
from django.core.exceptions import ValidationError

from webapp.models import Article, Comment, Tag


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['created_at', 'updated_at']


class ArticleTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        exclude = ['created_at']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['created_at', 'updated_at']


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")


class FullSearchForm(forms.Form):
    text = forms.CharField(max_length=100, required=False, label="По тексту")
    in_title = forms.BooleanField(initial=True, required=False, label="В заголовке")
    in_text = forms.BooleanField(initial=True, required=False, label="В тексте")
    in_tags = forms.BooleanField(initial=True, required=False, label="В тегах")
    in_comment_text = forms.BooleanField(initial=False, required=False, label="В комментариях")

    author = forms.CharField(max_length=100, required=False, label="По автору")
    article_author = forms.BooleanField(initial=True, required=False, label="Статьи")
    comment_author = forms.BooleanField(initial=False, required=False, label="Комментария")

    def clean(self):
        super().clean()
        data = self.cleaned_data
        if data.get('text'):
            if not (data.get('in_title') or data.get('in_text')
                    or data.get('in_tags') or data.get('in_comment_text')):
                raise ValidationError(
                    'One of the following checkboxes should be checked: In title, In text, In tags, In comment text',
                    code='text_search_criteria_empty'
                )

        elif data.get('author'):
            if not (data.get('article_author') or data.get('comment_author')):
                raise ValidationError(
                    'One of the following checkboxes should be checked: In article, In comment',
                    code='author_search_criteria_empty'
                )

        return data
