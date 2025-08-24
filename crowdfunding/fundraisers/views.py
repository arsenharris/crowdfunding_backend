from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Fundraiser , Pledge, Comment
from .serializers import CommentSerializer, FundraiserSerializer , PledgeSerializer , FundraiserDetailSerializer , CommentSerializer 
from django.db.models import Q  # this is for sseach function

class FundraiserList(APIView):
    def get(self, request):
        fundraisers = Fundraiser.objects.all()
        search_query = request.query_params.get('search', None) # self.request is the HTTP request object that triggers the view. .query_param contains all GET query parameters and . last piece tries to get value of the search and if it doesnt exist return to none. 
        if search_query:
            fundraisers = fundraisers.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
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
    def get_object(self, pk):
        try:
            fundraiser = Fundraiser.objects.get(pk=pk)
            return fundraiser
        except Fundraiser.DoesNotExist:
            raise Http404
    def get (self,request,pk):
        fundraiser = self.get_object(pk)
        serializer = FundraiserDetailSerializer(fundraiser)
        return Response(serializer.data)
    

class PledgeList(APIView):
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


class CommentList(APIView):
    def get (self,request):
        comments= Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    

    def get_comments (self):
        fundraiser_id = self.kwargs.get('fundraiser_id')
        comments = Comment.objects.filter(fundraiser_id=fundraiser_id)  
        return comments

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
