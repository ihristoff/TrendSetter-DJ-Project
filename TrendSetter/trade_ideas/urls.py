from django.urls import path

from TrendSetter.trade_ideas.views import CreateIdeaView, TradeIdeasDashboardView, DeleteTradeIdeaView

urlpatterns =(
    path('share/', CreateIdeaView.as_view(), name ='create idea'),
    path('ideas/', TradeIdeasDashboardView.as_view(), name='trade ideas dashboard'),
    path('delete/<int:pk>', DeleteTradeIdeaView.as_view(), name='delete idea'),

)