from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Social Network')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/', include('jwt_auth.urls')),
    path('api/', include('analytics.urls')),
    path('docs/', schema_view)
]
