from TrendSetter.accounts import forms
from TrendSetter.ratings.models import CommentRating


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentRating
        fields = ['comment', 'rating']