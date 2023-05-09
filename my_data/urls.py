from django.urls import path
from .views import *
urlpatterns = [

    # homepage
    path('', home, name="homepage"),
    path('login/', login_view, name="login"),
    path('logout', logout_view, name="logout"),

    path('user/create/', create_user, name="create-user"),
    path('user/list/', UserList.as_view(), name="user-list"),

    # for project/
    
    path('project/activities/', ProjectActivityListView.as_view(), name='project-activity-list'),
    path('list/', ProjectListView.as_view(), name='project-list'),
    path('create/project/', ProjectCreateView.as_view(), name='project-create'),
    path('update/<int:pk>/', ProjectUpdateView.as_view(), name='project-update'),
    path('delete/<int:pk>/', ProjectDeleteView.as_view(), name='project-delete'),

    #for activity


    # for event
    path('event/create', EventCreateView.as_view(), name='event-create'),
    path('event/list/', EventListView.as_view(), name='event-list'),
    path('event/update/<int:pk>/', EventUpdateView.as_view(), name='event-update'),
    path('event/delete/<int:pk>/', EventDeleteView.as_view(), name='event-delete'),


    path('event/<int:id>/participant/list', participant_view, name="participant-view"),
    path('event/participant/update/<int:pk>', ParticipantEditView.as_view(), name="participant-update"),
    path('event/participant/delete/<int:pk>', ParticipantDeleteView.as_view(), name='participants-delete'),


    path('activities/', ActivityListView.as_view(), name='activity-list'),
    path('datalist/', DataListView.as_view(), name='data-list'),
    path('api/age/ethnicity/datalist/', AgeEthnicityDataList.as_view(), name='age-ethnicity-datalist'),
    path('api/category/ethnicity/datalist/', CategoryEthnicityDataList.as_view(), name='category-ethnicity-datalist'),

    # path('participation/category', ParticipationCategoryList.as_view(), name="participation-category")

    # category_data
    path('list/age/ethnicity/', filter_age_and_ethnicity, name='list-age-ethnicity'),
    path('list/category/', filter_category, name='list-category'),
    path('data/visualize/', visualization_page, name='visualization-page'),

    
]
