from django.urls import path
from . import views
from .views import*
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path('index', views.index, name='index'),
    path('volunteers/', views.get_volunteers, name='get_volunteers'),
    path('markers/', views.get_markers, name='get_markers'),
    path('missingpl/<int:person_id>', views.show_missing_person_map, name='get_markers'),
    path('save-location/', views.save_location, name='save_location'),
    path('get-user-locations/', views.get_active_user_locations, name='get_user_locations'),
    # CATEGORY URLS
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    # APPLY HELP URLS
    path('help_list/', HelpListView.as_view(), name='help_list'),
    path('applyhelps/create/', ApplyHelpCreateView.as_view(), name='applyhelp_create'),
    path('applyhelps/<int:pk>/update/', ApplyHelpUpdateView.as_view(), name='applyhelp_update'),
    path('applyhelps/<int:pk>/delete/', ApplyHelpDeleteView.as_view(), name='applyhelp_delete'),

    # APPLICATION URLS
    path('applications/', ApplicationListView.as_view(), name='application_list'),
    path('applications/create/', ApplicationCreateView.as_view(), name='application_create'),
    path('applications/<int:pk>/update/', ApplicationUpdateView.as_view(), name='application_update'),
    path('applications/<int:pk>/delete/', ApplicationDeleteView.as_view(), name='application_delete'),

    # CHARITY COMPANY URLS
    path('charitycompanies/', CharityCompanyListView.as_view(), name='charitycompany_list'),
    path('charitycompanies/create/', CharityCompanyCreateView.as_view(), name='charitycompany_create'),
    path('charitycompanies/<int:pk>/update/', CharityCompanyUpdateView.as_view(), name='charitycompany_update'),
    path('charitycompanies/<int:pk>/delete/', CharityCompanyDeleteView.as_view(), name='charitycompany_delete'),

    # APPLICATION CHARITY URLS
    path('applicationcharities/', ApplicationCharityListView.as_view(), name='applicationcharity_list'),
    path('applicationcharities/create/', ApplicationCharityCreateView.as_view(), name='applicationcharity_create'),
    path('applicationcharities/<int:pk>/update/', ApplicationCharityUpdateView.as_view(), name='applicationcharity_update'),
    path('applicationcharities/<int:pk>/delete/', ApplicationCharityDeleteView.as_view(), name='applicationcharity_delete'),

    # USER LOCATION URLS
    path('userlocations/', UserLocationListView.as_view(), name='userlocation_list'),
    path('userlocations/create/', UserLocationCreateView.as_view(), name='userlocation_create'),
    path('userlocations/<int:pk>/update/', UserLocationUpdateView.as_view(), name='userlocation_update'),
    path('userlocations/<int:pk>/delete/', UserLocationDeleteView.as_view(), name='userlocation_delete'),

    # MARKER URLS
    path('markers/', MarkerListView.as_view(), name='marker_list'),
    path('markers/create/', MarkerCreateView.as_view(), name='marker_create'),
    path('markers/<int:pk>/update/', MarkerUpdateView.as_view(), name='marker_update'),
    path('markers/<int:pk>/delete/', MarkerDeleteView.as_view(), name='marker_delete'),
    path('missing_people/', MissingPersonListView.as_view(), name='missing_person_list'),
]
