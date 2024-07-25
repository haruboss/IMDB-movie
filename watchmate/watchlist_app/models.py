from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
class StreamPlatform(models.Model):
    name = models.CharField(max_length=30)
    about = models.CharField(max_length=150)
    website = models.URLField(max_length=50)
    
    def __str__(self):
        return self.name

class WatchList(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.TextField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    avg_rating = models.FloatField(default=0)
    total_rating = models.IntegerField(default=0)
    stream = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name='watchlist')
    def __str__(self):
        return self.title
    
class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="reviews")
    
    def __str__(self):
        return f'{self.watchlist} - [{self.rating}] {self.description}'