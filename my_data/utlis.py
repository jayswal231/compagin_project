from .models import * 
from django.db.models import Count
from django.db.models import Case, When, Value, CharField,IntegerField,F
from django.db.models.functions import Cast 

def generate_ethnicity_based_data(activities):
    data = []
    participant_age_groups = []
    for activity in activities:
        age_groups = [(0,5,'0-5'), (6,10,'6-10'), (11,18,'11-18'), (19,31,'19-31'), (32, 150,'31-above')]

        participant_age_groups = Participants.objects.filter(event__activity=activity).annotate(
            age_group=Case(
                *[When(
                    age__range=(start, end),
                    then=Value(label)
                ) for start, end, label in age_groups],
                output_field=CharField()
            ),
            age_int=Cast(F('age'), output_field=IntegerField())  # Convert age to integer
        ).values('ethnicity', 'age_group', 'age_int', 'gender')
    
    data = {}
    try:
        for p in participant_age_groups:
            if p['ethnicity'] not in data:
                data[p['ethnicity']] = {}
            if p['age_group'] not in data[p['ethnicity']]:
                data[p['ethnicity']][p['age_group']] = {'male': 0, 'female': 0, 'trans_sex': 0}
            if 'male' not in data[p['ethnicity']][p['age_group']]:
                data[p['ethnicity']][p['age_group']]['male'] = 0
            if 'female' not in data[p['ethnicity']][p['age_group']]:
                data[p['ethnicity']][p['age_group']]['female'] = 0
            if 'trans_sex' not in data[p['ethnicity']][p['age_group']]:
                data[p['ethnicity']][p['age_group']]['trans_sex'] = 0
                
            if p['gender'] == 'male':
                data[p['ethnicity']][p['age_group']]['male'] += 1
            elif p['gender'] == 'female':
                data[p['ethnicity']][p['age_group']]['female'] += 1
            else:
                data[p['ethnicity']][p['age_group']]['trans_sex'] += 1
        
        # loop over all age groups, and add them to the data with count=0 if they don't already exist
        for start, end, label in age_groups:
            for ethnicity in data:
                if label not in data[ethnicity]:
                    data[ethnicity][label] = {'male': 0, 'female': 0, 'trans_sex': 0}

        sorted_ethnicity_data = {}
        for ethnicity, age_data in data.items():
            sorted_age_data = sorted(age_data.items(), key=lambda x: int(x[0].split('-')[0]))
            sorted_ethnicity_data[ethnicity] = dict(sorted_age_data)

        age_data = [{'age': label, 'count': Participants.objects.filter(age__range=(start, end)).count()} for start, end, label in age_groups]
        final_data = {'age_data': age_data, 'ethnicity_data': sorted_ethnicity_data}
        
        return final_data
    except:
        return {}
        

def generate_category_based_data(activities):
    categories = ParticipationCategory.objects.all()
    data = []
    # activities=Activity.objects.all()
    for activity in activities:
        for category in categories:
            category_data = {'category': category.name, 'ethnicities': {}}
            participants = Participants.objects.filter(participation_category=category, event__activity=activity)
            for p in participants:
                if p.ethnicity not in category_data['ethnicities']:
                    category_data['ethnicities'][p.ethnicity] = {'male': 0, 'female': 0, 'trans_sex':0}
                if p.gender == 'male':
                    category_data['ethnicities'][p.ethnicity]['male'] += 1
                elif p.gender == 'female':
                    category_data['ethnicities'][p.ethnicity]['female'] += 1
                else:
                    category_data['ethnicities'][p.ethnicity]['trans_sex'] += 1
            data.append(category_data)

    for item in data:
        current_eth =list(item["ethnicities"].keys())
        not_present_eth_lower = [key.lower() for key in current_eth]
        not_present_eth = [item for item in Participants.get_ethnicity_choices() if item[0] not in not_present_eth_lower]
        
        for eth in not_present_eth:
            item["ethnicities"].update({eth[0]: {'male': 0, 'female': 0, 'trans_sex':0}})

    return data