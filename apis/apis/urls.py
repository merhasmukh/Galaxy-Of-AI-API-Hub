"""
URL configuration for apis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import RootView
# Swagger UI
schema_view = get_schema_view(
   openapi.Info(
      title="Django API Hub",
      default_version='v1',
      description="APIs",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="mhgn0001@gmail.com"),
      license=openapi.License(name="Public Licence"),
   ),
   public=True,
)

urlpatterns = [
    path('', RootView.as_view(), name='root'), 
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]
