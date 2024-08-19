from django.urls import path
from college.views import *
urlpatterns = [

    # Employee
    path("add-employee/",EmployeeViewSet.as_view({"post":"create"})),
   
    # college
    path("college/", CollegeViewSet.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("college/<uuid:uid>/", CollegeViewSet.as_view({"get": "retrieve",  "patch": "partial_update", "delete": "destroy"}), name="college-detail"),

    # capus
    path("campus/", CampusViewSet.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("campus/<uuid:uid>/", CampusViewSet.as_view({"get": "retrieve",  "patch": "partial_update", "delete": "destroy"}), name="college-detail"),

    #Faculty

    path("faculty/", FacultyViewSet.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("faculty/<uuid:uid>/", FacultyViewSet.as_view({"get": "retrieve",  "patch": "partial_update", "delete": "destroy"}), name="college-detail"),
 
    #Student

    path("student/", StudentViewSet.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("student/<uuid:uid>/", StudentViewSet.as_view({"get": "retrieve",  "patch": "partial_update", "delete": "destroy"}), name="college-detail"),


    #Washine-Mashine

    path("washing-mashine/", WashingMashineViewSet.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("washing-mashine/<uuid:uid>/", WashingMashineViewSet.as_view({"get": "get",  "patch": "update", "delete": "delete"}), name="college-detail"),

    #Drying-Mashine

    path("drying-mashine/", DryingMashineViewSet.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("drying-mashine/<uuid:uid>/", DryingMashineViewSet.as_view({"get": "get",  "patch": "update", "delete": "delete"}), name="college-detail"),


    #Vehicle expenses

    path("vehicle-expenses/", VehicleExpensesViewSet.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("vehicle-expenses/<uuid:uid>/", VehicleExpensesViewSet.as_view({"get": "retrieve",  "patch": "partial_update", "delete": "destroy"}), name="college-detail"),

    #Vehicle

    path("vehicle/", VehicleViewSet.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("vehicle/<uuid:uid>/", VehicleViewSet.as_view({"get": "retrieve",  "patch": "partial_update", "delete": "destroy"}), name="college-detail"),

    #folding table

    path("folding-table/", FoldingTableViewSet.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("folding-table/<uuid:uid>/", FoldingTableViewSet.as_view({"get": "retrieve",  "patch": "partial_update", "delete": "destroy"}), name="college-detail"),

    #complaint

    path("complaint/", ComplaintViewSet.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("complaint/<uuid:uid>/", ComplaintViewSet.as_view({"get": "retrieve",  "patch": "partial_update", "delete": "destroy"}), name="college-detail"),


]