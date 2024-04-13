from django.urls import path

from TrendSetter.trade_ideas.views import CreateIdeaView, TradeIdeasDashboardView, DeleteTradeIdeaView,TradeIdeaDetailView


urlpatterns =(
    path('share/', CreateIdeaView.as_view(), name ='create idea'),
    path('ideas/', TradeIdeasDashboardView.as_view(), name='trade ideas dashboard'),
    path('ideas/<int:idea_pk>', TradeIdeaDetailView.as_view(), name='details idea'),
    path('delete/<int:pk>', DeleteTradeIdeaView.as_view(), name='delete idea'),

)