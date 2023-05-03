import json
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import *
# Create your views here.

# for Project 
class ProjectListView(ListView):
    model = Project
    template_name = 'my_data/dashboard.html'

class ProjectCreateView(CreateView):
    model = Project
    fields = ['code', 'name']
    template_name = 'data_entry_list.html'
    success_url = reverse_lazy('project-list')

class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['code', 'name']
    template_name = 'data_entry.html'
    success_url = reverse_lazy('project-list')

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'dashboard.html'
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
        
        Event.objects.create(
        project= Project.objects.get(id=1),
        activity= Activity.objects.get(code=activity_code),
        start_date = request.POST.get('start_date'),
        end_date = request.POST.get('end_date'),
        province = request.POST.get('province'),
        district = request.POST.get('district'),
        palika = request.POST.get('palika'),
        ward = request.POST.get('ward'))

        return redirect('event-list')
        

class EventUpdateView(UpdateView):
    model = Event
    fields = "__all__"
    template_name = 'my_data/event_form.html'
    success_url = reverse_lazy('event-list')


def participant_view(request, id=None):
    template_name = "my_data/data_entry.html"
    return render(request, template_name)


class ParticipantEditView(UpdateView):
    model = Participants
    fields = "__all__"
    template_name = "my_data/participant_form.html"
    success_url = reverse_lazy('participant-view')
    



#for activity api
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Activity

class ActivityListView(APIView):
    def get(self, request):
        activities = Activity.objects.all()
        data = [{'code': activity.code, 'name':activity.name} for activity in activities]
        return Response(data)
    

# for province, district , palika api
class DataListView(APIView):
    def get(self, request):
        palikas = Palika.objects.all()
        districts = District.objects.all()
        provinces = Province.objects.all()
        result = {}
        for palika in palikas:
            province_name=palika.district.province.name
            district_name = palika.district.name
            palika_name=palika.name
            
            if province_name not in result:
                result[province_name] = {}
                result[province_name]["districts"] = {}
            if district_name not in result[province_name]["districts"]: 
                result[province_name]["districts"][district_name] = {}
                result[province_name]["districts"][district_name]["palikas"] = []
            result[province_name]["districts"][district_name]["palikas"].append(palika_name) 
            

        #for province and  district
        # for district in districts:
        #     province_name = district.province.name
        #     district_name = district.name
        #     if province_name not in result:
        #         result[province_name] = {}
        #     if district_name not in result[province_name]:
        #         result[province_name]['name']=district_name


        #for province only
        # for province in provinces:
        #     province_name = province.name
        #     if province_name not in result:
        #         result['name']=province_name

        return Response({"provinces": result})

    