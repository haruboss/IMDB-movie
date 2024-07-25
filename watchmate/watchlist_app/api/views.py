from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.validators import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from watchlist_app.api.serializers import WatchlistSerializer, StreamPlatformSerializer, ReviewSerializer
from watchlist_app.models import StreamPlatform, WatchList, Review
from watchlist_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly


# django based methord

# def watchlist(_request):
#     movies = WatchList.objects.all()
#     response = {
#         "movies": list(movies.values())
#     }
#     return JsonResponse(response)

# def watchlist_details(_request, pk):
#     movie = WatchList.objects.get(pk=pk)
#     response = {
#         "name": movie.name,
#         "desciption": movie.description,
#         "active": movie.active
#         }
#     return JsonResponse(response)

# django based methord End.

# DRF Function based view 
# @api_view(['GET', 'POST'])
# def watchlist(request):
#     if request.method == 'GET':
#         movies = WatchList.objects.all()
#         serializer_data = WatchlistSerializer(movies, many=True).data
#         return Response(serializer_data)
#     if request.method == 'POST':
#         serializer = WatchlistSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save() 
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
             
# @api_view(['GET', 'PUT', 'DELETE'])
# def watchlist_details(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({"error": "Not found."},status=status.HTTP_404_NOT_FOUND)
#         serializer_data = WatchlistSerializer(movie).data
#         return Response(serializer_data)
#     if request.method == 'PUT':
#         try:
#             movie = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({"error": "Not found."},status=status.HTTP_404_NOT_FOUND)
#         serializer = WatchlistSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
    
#     if request.method == 'DELETE':
#         try:
#             movie = WatchList.objects.get(pk=pk)
#         except WatchList.DoesNotExist:
#             return Response({"error": "Not found."},status=status.HTTP_404_NOT_FOUND)
#         movie.delete()
#         return Response({"message": "Deleted successfully."})

# DRF Function based view End. 

    
# DRF [APIView] Class based view start.
class WatchListAV(APIView):
    def get(self, request):
            movies = WatchList.objects.all()
            serializer_data = WatchlistSerializer(movies, many=True).data
            return Response(serializer_data)
        
        
    def post(self, request):
        serializer = WatchlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
        
class WatchDetailAV(APIView):
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({"error": "Not found."},status=status.HTTP_404_NOT_FOUND)
        serializer_data = WatchlistSerializer(movie).data
        return Response(serializer_data)
    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchlistSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response({"message": "Deleted successfully."})
# DRF [APIView] Class based view End.


# DRF [GenericAPIView, with mixins] Class based view start.
class StreamPlatformList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [AdminOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        
class StreamPlatformDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
# DRF [GenericAPIView] Class based view End.

    
# DRF [Generic View] Class based view start.

class ReviewAllList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
 
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)
        
        review_user = self.request.user
        
        reviewer =  Review.objects.filter(review_user=review_user, watchlist=watchlist)
        if reviewer.exists():
            raise ValidationError("You have already reviewed this watch.")
        
        if watchlist.total_rating  == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2
        
        watchlist.total_rating += 1
        watchlist.save()
        serializer.save(watchlist=watchlist, review_user=review_user)
        
        
        
class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]
    