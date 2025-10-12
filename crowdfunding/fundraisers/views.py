from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets, filters
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from .models import Fundraiser , Pledge, Comment, Like
from .serializers import FundraiserSerializer , PledgeSerializer , FundraiserDetailSerializer , CommentSerializer 
from django.db.models import Q  # this is for search function
from .permissions import IsOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from django.urls import reverse
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
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



class FundraiserList(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
        ]
    

    def get(self, request):
        fundraisers = Fundraiser.objects.all()
        search_query = request.query_params.get('search', None) # self.request is the HTTP request object that triggers the view. .query_param contains all GET query parameters and . last piece tries to get value of the search and if it doesnt exist return to none. 
        if search_query:
            fundraisers = fundraisers.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
            page = LimitOffsetPagination()
            paginated_fundraisers = page.paginate_queryset(fundraisers, request)
            
        serializer = FundraiserSerializer(fundraisers, many=True)
        return Response(serializer.data)
    

    def post (self, request):
        serializer = FundraiserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST)

class FundraiserDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    def get_object(self, pk):
        try:
            fundraiser = Fundraiser.objects.get(pk=pk)
            self.check_object_permissions(self.request, fundraiser) # Check if the user has permission to access this object
            return fundraiser
        except Fundraiser.DoesNotExist:
            raise Http404
        
    def get (self,request,pk):
        fundraiser = self.get_object(pk)
        serializer = FundraiserDetailSerializer(fundraiser)
        return Response(serializer.data)
    
    def put(self,request,pk):
        fundraiser = self.get_object(pk)
        serializer = FundraiserDetailSerializer(
            instance= fundraiser, 
            data=request.data,
            partial=True # this allows partial updates, so you dont have to provide all fields when updating.
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    def delete(self, request, pk):
        fundraiser = self.get_object(pk)
        fundraiser.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FeaturedFundraiserList(APIView):
    def get(self, request):
        fundraisers = Fundraiser.objects.all()
        fundraisers = sorted( ###sorted is built-in function that sorts any iterable
            fundraisers, ### queryset from above
            key=lambda f: sum([p.amount for p in f.pledges.all()]) / f.goal if f.goal else 0, ### key is a function that serves as a basis for sorting. here we use a lambda function that calculates the progress of each fundraiser by summing the amounts of all its pledges and dividing by its goal. if the goal is None or 0, it returns 0 to avoid division by zero.
            reverse=True  # highest progress first
        )

        # Take only top 5
        fundraisers = fundraisers[:3]

        serializer = FundraiserSerializer(fundraisers, many=True)
        return Response(serializer.data)
    
class FundraiserViewSet(viewsets.ModelViewSet):
    queryset = Fundraiser.objects.all()
    serializer_class = FundraiserSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_open', 'owner__id']  # allows filtering by is_open and owner id
    search_fields = ['title', 'description']  # allows searching in title and description
    ordering_fields = ['goal', 'created_at']  # allows ordering by goal and created_at
    pagination_class = LimitOffsetPagination  # Use limit-offset pagination

class FundraiserLikeList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        """Return the fundraiser details including likes count"""
        fundraiser = get_object_or_404(Fundraiser, pk=pk)
        serializer = FundraiserSerializer(fundraiser)  # pass the fundraiser object, not likes
        return Response(serializer.data)

    def post(self, request, pk):
        """Toggle like/unlike for a fundraiser"""
        fundraiser = get_object_or_404(Fundraiser, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, fundraiser=fundraiser)

        if not created:
            like.delete()
            return Response({"status": "unliked"})
        return Response({"status": "liked"})


class PledgeList(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
        

    def get_object(self, pk):
        try:
            pledges = Pledge.objects.get(pk=pk)
            return pledges
        except Pledge.DoesNotExist:
            raise Http404

    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)
    
    def post (self,request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            fundraiser_id = request.data.get('fundraiser')

            ###make sure fundraiser exists
            try:
                fundraiser = Fundraiser.objects.get(id=fundraiser_id)
            except Fundraiser.DoesNotExist:
                return Response(
                    {'error': 'Fundraiser does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            ###prevent pledging to own fundraiser
            if fundraiser.owner == request.user:
                return Response(
                    {'error': 'You cannot pledge to your own fundraiser.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(supporter=request.user, fundraiser=fundraiser)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def put (self,request):
        pledges=self.get_object(request.data.get('id'))
        serializer = PledgeSerializer(
            instance=pledges,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CommentList(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_object(self, pk):
        try:
            comments = Comment.objects.get(pk=pk)
            self.check_object_permissions(self.request, comments)
            return comments
        except Comment.DoesNotExist:
            raise Http404

    def get (self,request,pk):
        comments= Comment.objects.filter(fundraiser_id=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post ( self,request,pk):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user, fundraiser_id=pk)
            return Response(
                serializer.data,
                status = status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class CommentDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    def get_object(self,pk):
        try:
            comments=Comment.objects.get(pk=pk)
            self.check_object_permissions(self.request, comments)
            return comments
        except Comment.DoesNotExist:
            raise Http404
        
    def get (self,request, pk): # to get a specific comment by its pk
        comments = self.get_object(pk)
        serializer = CommentSerializer(comments)
        return Response(serializer.data)
    
    def put(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentSerializer(
            instance=comment,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
