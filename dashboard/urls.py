from django.urls import path
from dashboard.views import *

urlpatterns = [
    path("collegeList/",CollegeListViewset.as_view({"get":"list"})),
    path("college/",CollegeListViewset.as_view({"post":"create"})),
    path("collectionList/",CollectionListViewSet.as_view({"get":"list"})),
    path("routeList/",RouteListDashboardViewset.as_view({"get":"list"})),
    path("college-details/<uuid:uid>/",CollegeListViewset.as_view({"get":"get"})),
    path("campus-details/<uuid:uid>/",CampusDetailsViewset.as_view({"get":"get"})),
    path("employee-details/<uuid:uid>/",EmployeeDetailsViewset.as_view({"get":"get"})),
    path("analytic/",AnalyticViewset.as_view({"get":"list"})),

    #

]