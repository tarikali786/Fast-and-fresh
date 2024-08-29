from django.urls import path
from dashboard.views import CollegeListViewset

urlpatterns = [
    path("collegeList/",CollegeListViewset.as_view({"get":"get"}))

]