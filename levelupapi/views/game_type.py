"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import GameType


class GameTypeView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game type

        Returns:
            Response -- JSON serialized game type
        """
        # ORM gets single game type from database base on primary key in the url
        game_type = GameType.objects.get(pk=pk)
        # sets serialized (converts data into a JSON string) data to variable
        serializer = GameTypeSerializer(game_type)
        # pass variable to the response as the body
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        # ORM method .all() gets the whole collection of objects from database
        game_types = GameType.objects.all()
        # sets serialized (converts data into a JSON string) data to variable, many=true  because the response is a tuple/list
        serializer = GameTypeSerializer(game_types, many=True)
        # pass variable to the response as the body
        return Response(serializer.data)


# The serializer class determines HOW the Python data should be serialized (converted) to be sent back to the client.
class GameTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:  # holds the configuration for the serializer
        model = GameType  # tell the serializer to use the gametype model
        fields = ('id', 'label')  # and to include id and the label fields
