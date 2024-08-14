from django.urls import path
from college.views import TestApi
urlpatterns = [
    path("",TestApi.as_view({"GET":"get"}))
]