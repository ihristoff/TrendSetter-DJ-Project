from django.urls import path

from TrendSetter.main import views
from TrendSetter.main.views import IndexView, about

urlpatterns =(
    path('', IndexView.as_view(), name='index'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms and conditions'),
)
