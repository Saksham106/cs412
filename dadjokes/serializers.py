from rest_framework import serializers
from .models import *


class JokeSerializer(serializers.ModelSerializer):
    '''
    A serializer for the Joke model.
    '''
    
    class Meta:
        model = Joke
        fields = ['id', 'text', 'contributor', 'created']
    
    def create(self, validated_data):
        '''
        Override the superclass method that handles object creation.
        '''
        print(f'JokeSerializer.create, validated_data={validated_data}.')
        return Joke.objects.create(**validated_data)


class PictureSerializer(serializers.ModelSerializer):
    '''
    A serializer for the Picture model.
    '''
    
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'contributor', 'created']

