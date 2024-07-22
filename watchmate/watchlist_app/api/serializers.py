from rest_framework import serializers
from watchlist_app.models import Movie

# notes:

# 1) serializers : below created serializers.Serializer and serializers.ModelSerializer both have the same result.
# just for the note ModelSerializer come up with in inbuild function to create and update operations.

# 2) handle validation:
#     1) field level validation can we handle like (validate_name, min_description)
#     2) object level validation can we handle like (validate)

def min_description(description):
        if len(description) < 5:
            raise serializers.ValidationError("Movie Description is too short.")
        return description
        
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField()
#     description = serializers.CharField(validators=[min_description])
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
        
#         instance.save()
#         return instance
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Movie Name and Description can not be same.")
#         return data
    
#     def validate_name(self, name):
#         if len(name) < 2:
#             raise serializers.ValidationError("Movie Name is too short.")
#         return name
    

class MovieSerializer(serializers.ModelSerializer):
    
    name_size = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = "__all__"
        # fields = ['id', 'name', 'description']
        # exludes = ['active']
        
    def get_name_size(self, data):
        return len(data.name)
        
        
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("Movie Name and Description can not be same.")
        return data
    
    def validate_name(self, name):
        if len(name) < 2:
            raise serializers.ValidationError("Movie Name is too short.")
        return name