from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from my_data.context_processors import my_context_processor

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
from django.contrib.auth import authenticate, login 
from django.contrib.auth import logout

from django.contrib.auth.models import User, Group
import csv
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
# Create your views here.
import csv
from django.http import JsonResponse
from .models import Province, District, Palika

# for upload scv data  into model : province, district, palika
def uploaddata(request):
    if request.method == 'POST':
        if Province.objects.exists() or District.objects.exists() or Palika.objects.exists():
            Province.objects.all().delete()
            District.objects.all().delete()
            Palika.objects.all().delete()

        csv_file = request.FILES['mydata.csv'] 
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)

        for row in reader:
            province, created = Province.objects.get_or_create(name=row['province'])
            district, created = District.objects.get_or_create(name=row['district'], province=province)
            palika, created = Palika.objects.get_or_create(name=row['palika'], district=district)

        provinces = Province.objects.all()
        districts = District.objects.all()
        palikas = Palika.objects.all()

        data = []
        for province in provinces:
            province_data = {
                'name': province.name,
                'districts': []
            }
            for district in province.district_set.all():
                district_data = {
                    'name': district.name,
                    'palikas': []
                }
                for palika in district.palika_set.all():
                    district_data['palikas'].append(palika.name)
                province_data['districts'].append(district_data)
            data.append(province_data)
        return JsonResponse({'data': data})
    return render(request, 'upload_data.html')


def home(request):
    template_name = "index.html"
    return render(request, template_name)

def login_view(request):
    template_name = "login.html"
    context = {}

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(user)
            login(request, user)
            return redirect('event-list')
        else:
            context["error"] = "Invalid Username or Password"
            
    return render(request, template_name, context)

def logout_view(request):
    logout(request)
    return redirect('homepage')

@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    template_name = "my_data/role_form.html"
    context = {}
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        role = request.POST["role"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        phone = request.POST["phone"]
        address = request.POST["address"]

        print(role)
        try:
            my_group = Group.objects.get(name=role)
            my_user = User.objects.create_user(
                username=username,
                email=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            my_user.groups.add(my_group)

            UserProfile.objects.create(user=my_user, phone=phone, address=address)
            
            context["message"] = "User Successfully Created"
        except:
            context["error"] = "Error Creating User"

        return redirect('user-list')


    return render(request, template_name)

class UserList(UserPassesTestMixin, ListView):
    model = User
    template_name ='my_data/user_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation to get the default context data
        context = super().get_context_data(**kwargs)
        
        # Add additional context data
        profile_data = UserProfile.objects.filter(user__in=self.object_list)
        context['profile'] = profile_data
        
        return context

    def test_func(self):
        return self.request.user.is_superuser


class ProjectListView(ListView):
    model = Project
    template_name = 'my_data/dashboard.html'


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for event in context['object_list']:
            days = (event.end_date - event.start_date).days
            event.days = days
        return context
    


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

    if currentEvent.submit_one:
        context["role_a_submitted"] = True
    else:
        context["role_a_submitted"] = False
    
    if currentEvent.submit_two:
        context["role_b_submitted"] = True
    else:
        context["role_a_submitted"] = False

    if currentEvent.submit_three:
        context["role_c_submitted"] = True
    else:
        context["role_a_submitted"] = False

    context["ethnicity_choices"] = Participants.get_ethnicity_choices()
    context["participants"] = Participants.objects.filter(event=currentEvent)
    context['participation_category_data'] = [
        obj.name for obj in ParticipationCategory.objects.all()]

    # using the form submission to create the participant data
    if request.method == "POST":
        print(request.POST)

        if "participant_submit" in request.POST:
            query_dict = request.POST.copy()
            normal_dict = {key: value for key, value in query_dict.items()}
            normal_dict.pop("csrfmiddlewaretoken")
            normal_dict.pop('participant_submit')

            participation_category_data = normal_dict["participation_category"]
            current_category = ParticipationCategory.objects.get(
                name=participation_category_data)
            normal_dict["participation_category"] = current_category
            Participants.objects.create(
                **normal_dict, event=currentEvent, step1_user=request.user)

            return redirect('participant-view', id)
        

        if "save_submit" in request.POST:
            if "save_submit" in request.POST:
                roles_data = my_context_processor(request)
                roles = roles_data["current_roles"]
            
                if 'Role A' in roles:
                    
                    # Assign values to normal_dict before using it
                    normal_dict = {key: value for key, value in request.POST.items()}
                    normal_dict.pop("csrfmiddlewaretoken")
                    normal_dict.pop('save_submit')
                    events = Event.objects.get(id=id)
                    events.submit_one = True
                    events.save()

                    # get all the data of the participants and then set the setp 1
                    all_participants = Participants.objects.filter(event=events)
                    all_participants.update(step1=True)

                    return redirect('participant-view', events.id)
                
                if 'Role B' in roles:
                    
                    # Assign values to normal_dict before using it
                    normal_dict = {key: value for key, value in request.POST.items()}
                    normal_dict.pop("csrfmiddlewaretoken")
                    normal_dict.pop('save_submit')
                    events = Event.objects.get(id=id)
                    events.submit_two = True
                    events.save()

                    # get all the data of the participants and then set the setp 1
                    all_participants = Participants.objects.filter(event=events)
                    all_participants.update(step2=True, step2_user=request.user)

                    return redirect('participant-view', events.id)
                
                if 'Role C' in roles:
                    
                    # Assign values to normal_dict before using it
                    normal_dict = {key: value for key, value in request.POST.items()}
                    normal_dict.pop("csrfmiddlewaretoken")
                    normal_dict.pop('save_submit')
                    events = Event.objects.get(id=id)
                    events.submit_three = True
                    events.save()

                    # get all the data of the participants and then set the setp 1
                    all_participants = Participants.objects.filter(event=events)
                    all_participants.update(step3=True, step3_user=request.user)

                    return redirect('participant-view', events.id)
                
            event = Event.objects.get(id=id)
            return redirect('participant-view', event.id)

               
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
    template_name = 'my_data/age_group_data.html'
    
    if request.GET.get('activity_id') != "all" or request.GET.get('activity_id') is not None:
        activities = Activity.objects.filter(id=request.GET.get('activity_id'))
    else:
        activities = Activity.objects.all()

    final_data = generate_ethnicity_based_data(activities)

    ethnicities = list(final_data['ethnicity_data'].keys())
    age_groups = [age_group['age'] for age_group in final_data['age_data']]
    transposed_data = {}

    for age_group in age_groups:
        age_data = {}
        for ethnicity in ethnicities:
            age_data[ethnicity] = {
                'male': final_data['ethnicity_data'][ethnicity][age_group]['male'],
                'female': final_data['ethnicity_data'][ethnicity][age_group]['female'],
                'trans_sex': final_data['ethnicity_data'][ethnicity][age_group]['trans_sex']
            }
        transposed_data[age_group] = age_data

    print(transposed_data)

  
    return render(request, template_name, {'final_data': transposed_data})




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


# api for project select
class ProjectActivityListView(APIView):

    def get(self,request):
        projects = Project.objects.all()
        data = []
        for project in projects:
            activities = Activity.objects.filter(project=project)
            activities_data = []
            for activity in activities:
                activities_data.append({
                    "id":activity.id,
                    "name":activity.name,
                    "code":activity.code
                })
            data.append({
                "project name": project.name,
                "activity_name": activities_data
            })
        return Response(data)
