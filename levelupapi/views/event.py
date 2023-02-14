"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game


class EventView(ViewSet):
    """Level up event view"""

    def retrieve(self, request, pk):
        """Handle GET requests for events

        Returns:
            Response -- JSON serialized events
        """
        # ORM gets single event from database base on primary key in the url
        event = Event.objects.get(pk=pk)
        # sets serialized (converts data into a JSON string) data to variable
        serializer = EventSerializer(event)
        # pass variable to the response as the body
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        # ORM method .all() gets the whole collection of objects from database
        event = Event.objects.all()

        # sets serialized (converts data into a JSON string) data to variable, many=true  because the response is a tuple/list
        serializer = EventSerializer(event, many=True)
        # pass variable to the response as the body
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized event instance
        """
        organizer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])

        event = Event.objects.create(
            organizer=organizer,
            name=request.data["name"],
            location=request.data["location"],
            date=request.data["date"],
            start_time=request.data["start_time"],
            end_time=request.data["end_time"],
            game=game,
            description=request.data["description"]
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)

# The serializer class determines HOW the Python data should be serialized (converted) to be sent back to the client.


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    class Meta:  # holds the configuration for the serializer
        model = Event  # tell the serializer to use the game model
        # and to include id and the label fields
        fields = ('id', 'organizer', 'name', 'location',
                  'date', 'start_time', 'end_time')
