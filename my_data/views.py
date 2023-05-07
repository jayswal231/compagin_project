from typing import Any
from django.db import models

from my_data.utlis import *
from .models import Activity
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from django.forms.models import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *
from django.db.models import Count
from django.db.models import Case, When, Value, CharField,IntegerField,F
from django.db.models.functions import Cast 
# Create your views here.

# for Project

class ProjectListView(ListView):
    model = Project
    template_name = 'my_data/dashboard.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     districts = District.objects.all()
    #     for district in districts:
    #         district_event_counts = Event.objects.filter(district=district).count()
    #         participate_count = 0
    #         events= Event.objects.filter(district=district)
    #         for event in events:
    #             participate = Participants.objects.filter(event=event).count()
    #             participate_count += participate
    #         print(participate_count)
    #         print(district_event_counts)

    #     context["participate_count"] = participate_count
    #     context["district_event_counts"] = district_event_counts

    #     return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     district_event_counts = Participants.objects.values('event__district').annotate(
    #         event_count=Count('event', distinct=True),
    #         participant_count=Count('id', distinct=True)
    #     )
    #     context['district_event_counts'] = district_event_counts
    #     return context

class ProjectCreateView(CreateView):
    model = Project
    fields = ['code', 'name']
    template_name = 'my_data/data_entry_list.html'
    success_url = reverse_lazy('project-list')


class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['code', 'name']
    template_name = 'my_data/data_entry.html'
    success_url = reverse_lazy('project-list')


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'my_data/dashboard.html'
    success_url = reverse_lazy('project-list')


# for event

class EventListView(ListView):
    model = Event
    template_name = 'my_data/data_entry_list.html'



class EventCreateView(CreateView):
    model = Event
    fields = "__all__"
    template_name = 'my_data/event_form.html'
    success_url = reverse_lazy('event-list')

    def post(self, request, *args, **kwargs):
        activity_code = self.request.POST.get('code')
        print(activity_code)

        current_event = Event.objects.create(
            project=Project.objects.get(id=1),
            activity=Activity.objects.get(code=activity_code),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            province=request.POST.get('province'),
            district=request.POST.get('district'),
            palika=request.POST.get('palika'),
            ward=request.POST.get('ward'),
            person_responsible=request.POST.get('person_responsible'),
            community=request.POST.get('community'))

        return redirect('participant-view', current_event.id)


class EventUpdateView(UpdateView):
    model = Event
    fields = "__all__"
    template_name = 'my_data/event_form.html'
    success_url = reverse_lazy('event-list')


def participant_view(request, id=None):
    template_name = "my_data/data_entry.html"
    context = {}

    currentEvent = Event.objects.get(id=id)
    context["current_event"] = currentEvent
    context["data_entry_page"] = True

    context["ethnicity_choices"] = Participants.get_ethnicity_choices()
    context["participants"] = Participants.objects.filter(event=currentEvent)
    context['participation_category_data'] = [
        obj.name for obj in ParticipationCategory.objects.all()]

    # using the form submission to create the participant data
    if request.method == "POST":
        query_dict = request.POST.copy()
        normal_dict = {key: value for key, value in query_dict.items()}
        normal_dict.pop("csrfmiddlewaretoken")

        participation_category_data = normal_dict["participation_category"]
        current_category = ParticipationCategory.objects.get(
            name=participation_category_data)
        normal_dict["participation_category"] = current_category
        Participants.objects.create(
            **normal_dict, event=currentEvent, step1_user=request.user)

        return redirect('participant-view', id)

    return render(request, template_name, context)


class EventDeleteView(DeleteView):
    model = Event
    template_name = 'my_data/event_confirm_delete.html'
    success_url = reverse_lazy('event-list')


class ParticipantEditView(UpdateView):
    model = Participants
    fields = ["name", "affiliated_org", "designation", "age", "gender", "ethnicity",
              "pwd", "participation_category", "contact", "email"]
    template_name = "my_data/participant_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['participation_category_data'] = ParticipationCategory.objects.all()
        context["ethnicity_choices"] = Participants.get_ethnicity_choices()
        return context

    def get_success_url(self):
        return reverse_lazy('participant-view', kwargs={'id': self.object.event.id})


class ParticipantDeleteView(DeleteView):
    model = Participants
    template_name = 'my_data/participants_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('participant-view', kwargs={'id': self.object.event.id})


# for activity api

# class ParticipationCategoryList(APIView):
#     def get(self, request):
#         queryset = ParticipationCategory.objects.all()
#         data = [obj.name for obj in queryset]
#         return Response(data)


class ActivityListView(APIView):
    def get(self, request):
        activities = Activity.objects.all()
        data = [{'code': activity.code, 'name': activity.name}
                for activity in activities]
        return Response(data)


# for province, district , palika api
class DataListView(APIView):
    
    def get(self, request):
        if request.GET.get('palika_id') == "all" or request.GET.get('palika_id') is None:
            palikas = Palika.objects.all()
        else:
            palikas = Palika.objects.filter(id=request.GET.get('palika_id'))

        # palikas = Palika.objects.all()
        districts = District.objects.all()
        provinces = Province.objects.all()
        result = {}
        for palika in palikas:
            province_name = palika.district.province.name
            district_name = palika.district.name
            palika_name = palika.name

            if province_name not in result:
                result[province_name] = {}
                result[province_name]["districts"] = {}
            if district_name not in result[province_name]["districts"]:
                result[province_name]["districts"][district_name] = {}
                result[province_name]["districts"][district_name]["palikas"] = []
            result[province_name]["districts"][district_name]["palikas"].append(
                palika_name)

        return Response({"provinces": result})
    


# filter age and ethnicity
def filter_age_and_ethnicity(request):
    template_name = 'my_data/category_data.html'
    
    if request.GET.get('activity_id') != "all" or request.GET.get('activity_id') is not None:
        activities = Activity.objects.filter(id=request.GET.get('activity_id'))
    else:
        activities = Activity.objects.all()

    final_data = generate_ethnicity_based_data(activities)        
    return render(request, template_name, {'final_data': final_data})




# filter category and ethnicity
def filter_category(request):
    template_name = 'my_data/category_data.html'

    if request.GET.get('activity_id') == "all" or request.GET.get('activity_id') is None:
        activities = Activity.objects.all()
    else:
        activities = Activity.objects.filter(id=request.GET.get('activity_id'))

    data = generate_category_based_data(activities)      
    context = {'data': data}
    print(data)
    return render(request, template_name, context)


def visualization_page(request):
    template_name = "my_data/visualization.html"
    return render(request, template_name)



# api for age ethnicity datalist
class AgeEthnicityDataList(APIView):
    def get(self,request):
        if request.GET.get('activity_id') == "all" or request.GET.get('activity_id') is  None:
            activities = Activity.objects.all()
            
        else:
            activities = Activity.objects.filter(id=request.GET.get('activity_id'))

        data=generate_ethnicity_based_data(activities)
        context = {'data':data}
        return Response(context)
    

# api for category ethinicity datalist
class CategoryEthnicityDataList(APIView):

    def get(self, request):
        if request.GET.get('activity_id') == "all" or request.GET.get('activity_id') is None:
            activities = Activity.objects.all()
        else:
            activities = Activity.objects.filter(id=request.GET.get('activity_id'))

        data = generate_category_based_data(activities)      
        context = {'data': data}
        print(data)
        return Response(context)


