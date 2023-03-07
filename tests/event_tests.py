import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Gamer, Game
from rest_framework.authtoken.models import Token


class EventTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'game_types', 'games', 'event']

    def setUp(self):
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_event(self):
        """
        Ensure we can create a new event.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/events"

        # Define the request body
        data = {
            "organizer": 1,
            "name": "Spongebob Party",
            "location": "Kyles House",
            "date": "2023-04-07",
            "start_time": "22:30",
            "end_time": "01:22",
            "game": 2,
            "description": "playing galaga all night losers!"
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["organizer"], 1)
        self.assertEqual(json_response["name"], "Spongebob Party")
        self.assertEqual(json_response["location"], "Kyles House")
        self.assertEqual(json_response["date"], "2023-04-07")
        self.assertEqual(json_response["start_time"], "22:30")
        self.assertEqual(json_response["end_time"], "01:22")
        self.assertEqual(json_response["game"], 2)
        self.assertEqual(json_response["description"],
                         "playing galaga all night losers!i")
