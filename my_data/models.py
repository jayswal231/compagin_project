from django.db import models

# Create your models here.
class Project(models.Model):
    code = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name
    
class Activity(models.Model):
    code = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=500)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Event(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True, blank=True)
    province = models.CharField(max_length=500)
    district = models.CharField(max_length=500)
    palika = models.CharField(max_length=500, blank=True)
    ward = models.IntegerField(null=True, blank=True)
    community = models.CharField(max_length=500, blank=True)
    start_date  = models.DateField()
    end_date = models.DateField()
    person_responsible = models.CharField(max_length=100, blank=True)

    

class Participants(models.Model):
    name = models.CharField(max_length=100)
    affiliated_org = models.CharField(max_length=500, blank=True)
    designation = models.CharField(max_length=500, blank=True)
    age = models.IntegerField(null=True, blank=True)
    GENDER = (("male", "male"),("female", "female"),("others", "others"))
    gender = models.CharField(max_length=500, choices=GENDER, default="male")
    ETHINICITY = (("dalit","dalit"),)
    ethinicity = models.CharField(max_length=500, choices=ETHINICITY, blank=True)
    pwd = models.BooleanField(null=True, blank=True)
    participation_category = models.CharField(max_length=1000, blank=True)
    contact = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    step1_user = models.CharField(max_length=500, null=True, blank=True)
    step1 = models.BooleanField(null=True,blank=True)
    step2_user = models.CharField(max_length=500, null=True, blank=True)
    step2 = models.BooleanField(null=True, blank=True)
    step3_user = models.CharField(max_length=500, null=True, blank=True)
    step3 = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class Actions(models.Model):
    participants = models.ForeignKey(Participants, on_delete=models.CASCADE, null=True, blank=True)
    ACTIONS = (("list","list"),("create","create"),("update","update"),("delete","delete"))
    actions = models.CharField(max_length=50, choices=ACTIONS, default="list")
    current_state = models.JSONField(null=True, blank=True)
    user = models.CharField(max_length=1000, null=True, blank=True)
    group = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.actions
    

class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
        

class District(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Palika(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name