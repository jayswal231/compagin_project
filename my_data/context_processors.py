from my_data.models import Participants, ParticipationCategory


def my_context_processor(request):
    roles = []
    for role in request.user.groups.all():
        roles.append(role.name)

    print(roles)

    ethnicities = Participants.get_ethnicity_choices()  
    categories = ParticipationCategory.objects.all()

    return {"current_roles": roles, 'ethnicities': ethnicities, "categories": categories}
