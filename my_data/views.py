from .models import Activity
from rest_framework.response import Response
from rest_framework.views import APIView
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
        palikas = Palika.objects.all()
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

        # for province and  district
        # for district in districts:
        #     province_name = district.province.name
        #     district_name = district.name
        #     if province_name not in result:
        #         result[province_name] = {}
        #     if district_name not in result[province_name]:
        #         result[province_name]['name']=district_name

        # for province only
        # for province in provinces:
        #     province_name = province.name
        #     if province_name not in result:
        #         result['name']=province_name

        return Response({"provinces": result})
