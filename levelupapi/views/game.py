"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType


class GameView(ViewSet):
    """Level up games view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single games

        Returns:
            Response -- JSON serialized games
        """
        # ORM gets single game from database base on primary key in the url
        game = Game.objects.get(pk=pk)
        # sets serialized (converts data into a JSON string) data to variable
        serializer = GameSerializer(game)
        # pass variable to the response as the body
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        # ORM method .all() gets the whole collection of objects from database
        game = Game.objects.all()
        # sets serialized (converts data into a JSON string) data to variable, many=true  because the response is a tuple/list
        serializer = GameSerializer(game, many=True)
        # pass variable to the response as the body
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(
            user=request.auth.user)  # we use the request.auth.user to get the Gamer object based on the user
        # retrieve game_type object from db
        game_type = GameType.objects.get(pk=request.data["game_type"])
        # The data passed in from the client is held in the request.data dictionary. Whichever keys are used on the request.data must match what the client is passing to the server.

        game = Game.objects.create(  # ORM .create method: pass the fields as parameters to the function
            name=request.data["name"],
            maker=request.data["maker"],
            number_of_players=request.data["number_of_players"],
            skill_level=request.data["skill_level"],
            gamer=gamer,
            game_type=game_type,
        )
        serializer = GameSerializer(game)
        return Response(serializer.data)


# The serializer class determines HOW the Python data should be serialized (converted) to be sent back to the client.
class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    class Meta:  # holds the configuration for the serializer
        model = Game  # tell the serializer to use the game model
        # and to include id and the label fields
        fields = ('id', 'name', 'game_type', 'gamer',
                  'maker', 'number_of_players', 'skill_level')
