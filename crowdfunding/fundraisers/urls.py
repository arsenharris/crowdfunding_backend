
from django.urls import path
from . import views

urlpatterns = [
    path("", views.api_root),
    path('fundraisers/', views.FundraiserList.as_view()),
    path('fundraisers/<int:pk>/', views.FundraiserDetail.as_view()),
    path('fundraisers/search/', views.FundraiserList.as_view()),
    # path('pledges/', views.PledgeList.as_view()),
    path('fundraisers/<int:pk>/pledges/', views.PledgeList.as_view()),
    path('fundraisers/<int:pk>/comments/', views.CommentList.as_view()),
    path('fundraisers/<int:pk>/likes/', views.FundraiserLikeList.as_view()),
    path('fundraisers/featured/', views.FeaturedFundraiserList.as_view()),

]   