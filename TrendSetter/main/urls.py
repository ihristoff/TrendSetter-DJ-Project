from django.urls import path

from TrendSetter.main import views
from TrendSetter.main.views import IndexView

urlpatterns =(
    path('', IndexView.as_view(), name='index'),
)
