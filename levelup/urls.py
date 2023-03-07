from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from levelupapi.views import register_user, login_user
from django.conf.urls import include
from rest_framework import routers
from levelupapi.views import GameTypeView, GameView, EventView


# tells the router to accept /gametypes instead of /gametypes/
router = routers.DefaultRouter(trailing_slash=False)
# r'gametypes, is setting up the url GameTypeVie.w is telling the server which view to use when it sees that url. gametype, is called the base name.
router.register(r'gametypes', GameTypeView, 'gametype')
router.register(r'games', GameView, 'game')
router.register(r'events', EventView, 'event')


urlpatterns = [
    # Requests to http://localhost:8000/register will be routed to the register_user function
    path('register', register_user),
    # Requests to http://localhost:8000/login will be routed to the login_user function
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include('levelupreports.urls')),
]
