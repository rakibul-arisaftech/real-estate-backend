"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view

from django.views.static import serve

schema_view = get_swagger_view(title='Real Estate API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('doc', schema_view),
    path("api/v2/", include("users.urls", namespace="users")),
    path("api/v2/post/", include("blog.urls", namespace="blog")),
    path('api/v2/', include('service.urls')),
    path('api/v2/', include('category.urls')),
    path('api/v2/', include('property.urls')),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'utils.views.error_404'
handler500 = 'utils.views.error_500'