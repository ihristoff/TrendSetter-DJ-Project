from django import forms
from django.http import HttpResponseRedirect

from .models import EducationalArticle, Comment, ArticleRating
from django import forms
from ckeditor.widgets import CKEditorWidget

class EducationalArticleForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = EducationalArticle
        fields = ['title', 'category', 'image','description']


    labels={
        'title':'Title',
        'category':'Category',
        'description':'Description',
    }

    help_texts = {
        'image': 'Upload image',
    }

    help_text = {
        'title':'Title',
        'image':'Image',
        'description':'Description'
    }


class EducationalArticleUpdateForm(EducationalArticleForm):
    pass

class CommentForm(forms.ModelForm):
    content = forms.CharField(label ="", widget = forms.Textarea(
    attrs ={
        'class':'form-control',
        'placeholder':'Your comment here !',
        'rows':4,
        'cols':50
    }))
    class Meta:
        model = Comment
        fields =['content']

class ArticleRatingForm(forms.ModelForm):
    class Meta:
        model = ArticleRating
        fields = ['rating']


class EducationalArticleFormDelete(forms.ModelForm):

    class Meta:
        model = EducationalArticle
        fields = ['title',]

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance

    def delete(self, request, *args, **kwargs):
        print("Delete method called")
        obj = self.get_object()
        obj.delete()
        return HttpResponseRedirect(self.get_success_url())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for (_, field) in self.fields.items():

            field.widget.attrs['readonly'] = 'readonly'