from django import forms
from .models import EducationalArticle

from django import forms
from .models import EducationalArticle, Gallery

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

