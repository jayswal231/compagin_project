from django.urls import path
from .views import *
urlpatterns = [
    # for project
    path('list/', ProjectListView.as_view(), name='project-list'),
    path('create/', ProjectCreateView.as_view(), name='project-create'),
    path('update/<int:pk>/', ProjectUpdateView.as_view(), name='project-update'),
    path('delete/<int:pk>/', ProjectDeleteView.as_view(), name='project-delete'),

    #for activity


    # for event
    path('event/create', EventCreateView.as_view(), name='event-create'),
    path('event/list', EventListView.as_view(), name='event-list'),
    path('event/update/<int:pk>/', EventUpdateView.as_view(), name='event-update'),
    path('event/delete/<int:pk>/', EventDeleteView.as_view(), name='event-delete'),


    path('event/<int:id>/participant/list', participant_view, name="participant-view"),
    path('event/participant/update/<int:pk>', ParticipantEditView.as_view(), name="participant-update"),
    path('event/participant/delete/<int:pk>', ParticipantDeleteView.as_view(), name='participants-delete'),


    path('activities/', ActivityListView.as_view(), name='activity-list'),
    path('datalist/', DataListView.as_view(), name='data-list'),
    # path('participation/category', ParticipationCategoryList.as_view(), name="participation-category")

    # category_data
    path('list/age/ethnicity/', filter_age_and_ethnicity, name='list-age-ethnicity'),
    path('list/category/', filter_category, name='list-category'),
    path('data/visualize/', visualization_page, name='visualization-page'),
]
