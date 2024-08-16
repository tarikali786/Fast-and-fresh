from django.urls import path
from college.views import *
urlpatterns = [

    # Employee
    path("add-employee/",EmployeeViewSet.as_view({"post":"create"})),
   
    # college
    path("college/", CollegeViewSet.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("college/<uuid:uid>/", CollegeViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="college-detail"),

    # capus
    path("campus/", CampusViewSet.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("campus/<uuid:uid>/", CampusViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="college-detail"),

    #Faculty

    path("faculty/", FacultyViewSet.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("faculty/<uuid:uid>/", FacultyViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="college-detail"),
 
    #Student

    path("student/", StudentViewSet.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("student/<uuid:uid>/", StudentViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="college-detail"),

]