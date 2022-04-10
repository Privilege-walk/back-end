from django.contrib import admin
from django.urls import path, include

from channels.routing import URLRouter

import walk.urls

# HTTP URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_mgmt.urls')),
    path('host/', include('host.urls')),
    path('walk/', include('walk.urls')),
]

# Websocket URLs
websocket_urlpatterns = URLRouter([
    path('ws/walk/', URLRouter(walk.urls.websocket_urlpatterns)),
])
