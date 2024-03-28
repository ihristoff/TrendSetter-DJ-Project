from django import forms
from .models import EducationArticle

from django import forms
from .models import EducationArticle, Gallery

class EducationArticleForm(forms.ModelForm):
    class Meta:
        model = EducationArticle
        fields = ['title', 'image','description']

    # gallery = forms.ImageField()


