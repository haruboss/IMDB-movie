from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review

# notes:

# 1) serializers : below created serializers.Serializer and serializers.ModelSerializer both have the same result.
# just for the note ModelSerializer come up with in inbuild function to create and update operations.

# 2) handle validation:
#     1) field level validation can we handle like (validate_name, min_description)
#     2) object level validation can we handle like (validate)

def min_description(description):
        if len(description) < 5:
            raise serializers.ValidationError("Description is too short.")
        return description
        
# class WatchlistSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField(validators=[min_description])
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         return WatchList.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
        
#         instance.save()
#         return instance
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and Description can not be same.")
#         return data
    
#     def validate_name(self, name):
#         if len(name) < 2:
#             raise serializers.ValidationError("Name is too short.")
#         return name
    
        
class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ('watchlist',)
        
class WatchlistSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True)
    # title_size = serializers.SerializerMethodField()
    class Meta:
        model = WatchList
        fields = "__all__"
        # fields = ['id', 'title', 'storyline']
        # exludes = ['active']
        
    def get_title_size(self, data):
        return len(data.title)
    
    def validate(self, data):
        if data['title'] == data['storyline']:
            raise serializers.ValidationError("Name and storyline can not be same.")
        return data
    
    def validate_name(self, title):
        if len(title) < 2:
            raise serializers.ValidationError("Name is too short.")
        return title
    
class StreamPlatformSerializer(serializers.ModelSerializer):
    
    # watchlist = WatchlistSerializer(many=True, read_only=True)
    # watchlist = serializers.StringRelatedField(many=True, read_only=True)
    # watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    watchlist = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='movie-details')
    
    
    
    class Meta:
        model = StreamPlatform
        fields = "__all__"
