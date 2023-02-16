"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game
from rest_framework.decorators import action


class EventView(ViewSet):
    """Level up event view"""

    def destroy(self, request, pk):
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

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
        gamer = Gamer.objects.get(user=request.auth.user)
        events = []
        events = Event.objects.all()
        # Set the `joined` property on every event
        for event in events:
            # Check to see if the gamer is in the attendees list on the event
            event.joined = gamer in event.attendees.all()

        # sets serialized (converts data into a JSON string) data to variable, many=true  because the response is a tuple/list
        serializer = EventSerializer(events, many=True)
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

    def update(self, request, pk):
        """Handle PUT requests for a event

        Returns:
            Response -- Empty body with 204 status code
        """

        # * get the object we want from the database
        event = Event.objects.get(pk=pk)
        # *the next lines are setting the fields on obj to the values coming from the client
        event.name = request.data["name"]
        event.location = request.data["location"]
        event.date = request.data["date"]
        event.start_time = request.data["start_time"]
        event.end_time = request.data["end_time"]
        event.description = request.data["description"]

        game = Game.objects.get(pk=request.data["game"])
        event.game = game
        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    # ? For this action, you want a client to make a request to allow a gamer to sign up for an event.
    # * Using the action decorator turns a method into a new route. In this case, the action will accept POST methods and because detail=True the url will include the pk. Since we need to know which event the user wants to sign up for we’ll need to have the pk. The route is named after the function. So to call this method the url would be http://localhost:8000/events/2/signup
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.add(gamer)
        return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Post request for a user to sign up for an event"""

        gamer = Gamer.objects.get(user=request.auth.user)
        event = Event.objects.get(pk=pk)
        event.attendees.remove(gamer)
        return Response({'message': 'Gamer removed'}, status=status.HTTP_201_CREATED)

# The serializer class determines HOW the Python data should be serialized (converted) to be sent back to the client.


class EventGameSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    class Meta:
        model = Game
        fields = ('id', 'name')


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for games
    """
    game = EventGameSerializer(serializers.ModelSerializer)

    class Meta:  # holds the configuration for the serializer
        model = Event  # tell the serializer to use the game model
        # and to include id and the label fields
        fields = ('id', 'game', 'organizer',
                  'description', 'date', 'start_time', 'end_time', 'attendees',
                  'joined')
