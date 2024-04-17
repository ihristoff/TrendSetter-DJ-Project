
from django import forms

from TrendSetter.trade_ideas.models import TradeIdea, Comment


class CreateTradeIdeaForm(forms.ModelForm):
    timeframe = forms.ChoiceField(
        choices=TradeIdea.TIMEFRAME_CHOICES,
        help_text="What is the horizon of your position?"
    )


    class Meta:
        model = TradeIdea
        fields = ("title", 'symbol', 'category','timeframe', "idea_image", "description")

        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Title"}),
            # "idea_image": forms.URLInput(attrs={"placeholder": "Share your screenshot"}),
            "description": forms.Textarea(attrs={"placeholder": "Describe your logic here"}),
            # "symbol": forms.TextInput(attrs={"placeholder": "Symbol"}),
            # "timeframe": forms.TextInput(attrs={"placeholder": "Horizon"}),

        }

        # labels = {
        #     "name": "Pet name",
        #     "pet_photo": "Link to image",
        # }

    # def __init__(self, *args, **kwargs):
    #     super(CreateTradeIdeaForm, self).__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].label = False


class  DeleteTradeIdeaForm(forms.ModelForm):
    class Meta:
        model = TradeIdea
        fields = ("title", 'symbol', 'timeframe', "idea_image")


#
class CommentIdeaForm(forms.ModelForm):
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
