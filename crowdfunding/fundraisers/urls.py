
from django.urls import path
from . import views
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        "message": "Welcome to Inkvestor API",
        "endpoints": [
            "/fundraisers/",
            "/pledges/",
            "/fundraisers/<id>/comments/",
        ]
    })
urlpatterns = [
    path("", views.api_root(), ),
    path('fundraisers/', views.FundraiserList.as_view()),
    path('fundraisers/<int:pk>/', views.FundraiserDetail.as_view()),
    path('fundraisers/search/', views.FundraiserList.as_view()),
    path('pledges/', views.PledgeList.as_view()),
    path('fundraisers/<int:pk>/comments/', views.CommentList.as_view()),
    path('fundraisers/<int:pk>/likes/', views.FundraiserLikeList.as_view()),
    path('fundraisers/featured/', views.FeaturedFundraiserList.as_view()),

]   