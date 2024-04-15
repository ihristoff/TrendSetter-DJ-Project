from django import forms
from .models import EducationalArticle, Comment, ArticleRating
from django import forms
from ckeditor.widgets import CKEditorWidget

class EducationalArticleForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = EducationalArticle
        fields = ['title', 'image','description']

    # gallery = forms.ImageField()

    # labels={
    #     'title':'',
    #     'image':'',
    #     'description':'',
    # }
    #
    # help_texts = {
    #     'image': 'Upload image',
    # }

    # help_text = {
    #     'title':'Title',
    #     'image':'Image',
    #     'description':'Des Long'
    # }


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
        fields = ['title', 'image']

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance

    def delete(self, request, *args, **kwargs):
        print("Delete method called")
        obj = self.get_object()
        obj.delete()
        return HttpResponseRedirect(self.get_success_url())