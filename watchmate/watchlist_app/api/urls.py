from django.urls import path
from .views import WatchListAV, WatchDetailAV, StreamPlatformList, StreamPlatformDetail, ReviewList, ReviewDetail, ReviewAllList, ReviewCreate
urlpatterns = [
    
    # route for django and DRF function based view
    # path('list/', watchlist, name='movie-list'),
    # path('<int:pk>', watchlist_details, name='movie-details'),
    
    
    # DRF APIView routes
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='movie-details'),
    
    # DRF GenericAPIView with mixins routes
    path('stream', StreamPlatformList.as_view(), name='stream-list'),
    path('stream/<int:pk>/', StreamPlatformDetail.as_view(), name='stream-detail'),
    
    # DRF GenericAPIView routes
    path('review/all', ReviewAllList.as_view(), name='review-list'),
    
    path('<int:pk>/create-review/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
]
