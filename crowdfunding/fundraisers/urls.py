from django.urls import path
from . import views

urlpatterns = [
    path('fundraisers/', views.FundraiserList.as_view()),
    path('fundraisers/<int:pk>/', views.FundraiserDetail.as_view()),
    path('fundraisers/search/', views.FundraiserList.as_view()),
    path('pledges/', views.PledgeList.as_view()),
    path('fundraisers/<int:fundraiser_id>/comments/', views.CommentList.as_view()),

]   