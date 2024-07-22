from django.shortcuts import render
from watchlist_app.api.serializers import MovieSerializer
from watchlist_app.models import Movie
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view


# django based methord
# def movie_list(_request):
#     movies = Movie.objects.all()
#     response = {
#         "movies": list(movies.values())
#     }
#     return JsonResponse(response)

# def movie_details(_request, pk):
#     movie = Movie.objects.get(pk=pk)
#     response = {
#         "name": movie.name,
#         "desciption": movie.description,
#         "active": movie.active
#         }
#     return JsonResponse(response)

# django based methord End.

# DRF Function based view 
# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer_data = MovieSerializer(movies, many=True).data
#         return Response(serializer_data)
#     if request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save() 
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
             
# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({"error": "Movie not found."},status=status.HTTP_404_NOT_FOUND)
#         serializer_data = MovieSerializer(movie).data
#         return Response(serializer_data)
#     if request.method == 'PUT':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({"error": "Movie not found."},status=status.HTTP_404_NOT_FOUND)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
    
#     if request.method == 'DELETE':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({"error": "Movie not found."},status=status.HTTP_404_NOT_FOUND)
#         movie.delete()
#         return Response({"message": "Movie Deleted successfully."})

# DRF Function based view End. 

    
# DRF Class based view 
class MovieListAV(APIView):
    def get(self, request):
            movies = Movie.objects.all()
            serializer_data = MovieSerializer(movies, many=True).data
            return Response(serializer_data)
        
        
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

            
class MovieDetailAV(APIView):
    def get(self, request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found."},status=status.HTTP_404_NOT_FOUND)
        serializer_data = MovieSerializer(movie).data
        return Response(serializer_data)
    def put(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        movie = Movie.objects.get(pk=pk)
        movie.delete()
        return Response({"message": "Movie Deleted successfully."})

# DRF Class based view End
    