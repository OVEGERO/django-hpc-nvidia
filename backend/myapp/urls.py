from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.documentation import include_docs_urls

router = routers.DefaultRouter()

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('', views.filters_view, name='filters'),
    path('docs/', include_docs_urls(title='Django CRUD API', description='RESTful API for managing tasks.')),
]
