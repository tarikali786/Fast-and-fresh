from django.urls import path
from college.views import *
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [

    # Employee
    path("add-employee/",EmployeeViewSet.as_view({"post":"create"})),
    path("login/",EmployeeSignInViewset.as_view({"post":"post"})),
    path("logout/",EmployeeLogoutViewset.as_view({"post":"logout"})),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path("all-employee/",AllEmployeeViewset.as_view({"get":"get"})),

    

   
    # college
    path("college/", CollegeViewSet.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("college/<uuid:uid>/", CollegeViewSet.as_view({"get": "retrieve",  "patch": "partial_update", "delete": "destroy"}), name="college-detail"),

    # college
    path("routes/", RoutesViewSet.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("routes/<uuid:uid>/", RoutesViewSet.as_view({"get": "retrieve",  "patch": "partial_update", "delete": "destroy"}), name="college-detail"),

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

    #StudentDaySheet

    path("student-daysheet/", StudentDaySheetViewset.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("student-daysheet/<uuid:uid>/", StudentDaySheetViewset.as_view({"get": "retrieve",  "patch": "partial_update", "delete": "destroy"}), name="college-detail"),

    #FacultyDaySheet

    path("faculty-daysheet/", FacultyDaySheetViewset.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("faculty-daysheet/<uuid:uid>/", FacultyDaySheetViewset.as_view({"get": "retrieve",  "patch": "partial_update", "delete": "destroy"}), name="college-detail"),
    
    #Student Remark

    path("student-remark/", StudentRemarkViewset.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("student-remark/<uuid:uid>/", StudentRemarkViewset.as_view({"get": "retrieve",  "patch": "partial_update", "delete": "destroy"}), name="college-detail"),

    #RemarkByWarehouse

    path("remark-by-whare-house/", RemarkByWarehouseViewset.as_view({"get": "list", "post": "create"}), name="college-list-create"),
    path("remark-by-whare-house/<uuid:uid>/", RemarkByWarehouseViewset.as_view({"get": "retrieve",  "patch": "partial_update", "delete": "destroy"}), name="college-detail"),


    #collection

    path("collection/", CollectionViewSet.as_view({ "post": "create","get":"list"}), name="college-list-create"),
    path("collection/<uuid:uid>/", CollectionViewSet.as_view({"get": "retrieve",  "patch": "update", "delete": "delete"}), name="college-detail"),


    # Mics
    path("get-campus-details/<uuid:uid>/",GetCampusDetailsByUIDsViewset.as_view({"get":"get"})),
    path("get-faculty-list/<uuid:uid>/",GetFacultyListViewset.as_view({"get":"get"})),
    path("get-employee-collection-list/<uuid:uid>/",GetEmployeeCollectionsViewset.as_view({"get":"get"})),
    path("get-studnet-details/",GetStudentDetailsViewset.as_view({"post":"post"})),
    path("get-latest-collection/",LatestCollectionViewset.as_view({"get":"get"})),
    path("get-non-delivered-student-daysheet-collection/",FilterCollectionsByStudentViewset.as_view({"post":"post"})),


]