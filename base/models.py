from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=100,null=True, unique=True)
    email = models.EmailField(max_length=100,null=True)
    bio = models.TextField(max_length=500,null=True)
    avatar = models.TextField(null=True,blank=True)
    location = models.CharField(max_length=50,null=True)
    company = models.CharField(max_length=50,null=True)
    followers=models.IntegerField(default=0)
    following=models.IntegerField(default=0)
    public_repos=models.IntegerField(default=0)
    invites = models.ManyToManyField('Team', related_name='invites', blank=True)
    teams=models.ManyToManyField('Team', related_name='teams', blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.username
    
class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    teamleader = models.ForeignKey(User, related_name='teamleader', on_delete=models.CASCADE)
    invited_members = models.ManyToManyField(User, related_name='invited_members', blank=True)
    accepted_members = models.ManyToManyField(User, related_name='accepted_members', blank=True)
    def __str__(self):
        return self.name
    
    def get_hackathons(self):
        return Hackathon.objects.filter(teams=self)

    
class Hackathon(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    teams = models.ManyToManyField(Team)
    def __str__(self):
        return self.name

class Organization(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    email=models.EmailField(max_length=100)
    hackathons = models.ManyToManyField(Hackathon)
    password=models.CharField(max_length=100)
    image=models.ImageField(upload_to='images/',blank=True)
    def __str__(self):
        return self.name    

class Project(models.Model):
    pname = models.CharField(max_length=100)
    repo_url = models.CharField(max_length=200,blank=True)
    pteam = models.ForeignKey(Team, related_name='pteam', on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.pname
        
class Tags(models.Model):
    name = models.CharField(max_length=100)
    coder= models.ForeignKey(User, related_name='coder', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    message = models.CharField(max_length=500, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.message[0:69]

