from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from .models import Fundraiser , Pledge, Comment
from .serializers import FundraiserSerializer , PledgeSerializer , FundraiserDetailSerializer , CommentSerializer 
from django.db.models import Q  # this is for search function
from .permissions import IsOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import LimitOffsetPagination
from django.urls import reverse
from django.conf import settings


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

class PledgeList(APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
        

    def get_object(self, pk):
        try:
            pledges = Pledge.objects.get(pk=pk)
            self.check_object_permissions(self.request, pledges)
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
            serializer.save(supporter=request.user)
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
    
    def post ( self,request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
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

