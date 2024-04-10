from django import forms
from .models import EducationalArticle, Comment

from django import forms
from .models import EducationalArticle
class EducationalArticleForm(forms.ModelForm):
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