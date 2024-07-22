from django.urls import path
# from .views import movie_list, movie_details
from .views import MovieListAV, MovieDetailAV
urlpatterns = [
    
    # route for django and DRF function based view
    # path('list/', movie_list, name='movie-list'),
    # path('<int:pk>', movie_details, name='movie-details')
    
    
    # route for DRF Class based view
    path('list/', MovieListAV.as_view(), name='movie-list'),
    path('<int:pk>', MovieDetailAV.as_view(), name='movie-details')
    
    
    
]
