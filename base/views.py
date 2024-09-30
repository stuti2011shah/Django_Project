from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
from .models import Team, User, Project, Hackathon, Tags,Organization,Chat
from .predictor import recommend_users 
from django.db.models import Q

# Create your views here.

@login_required(login_url='/login/')
def home(request):
    git_user=request.user.username
    print(git_user)
    url = f"https://api.github.com/users/{git_user}"
    r = requests.get(url.format(git_user)).json()
    #print(r)
    #save in models
    Name = r['name']
    Bio = r['bio']
    Location = r['location']
    Company = r['company']
    Email = r['email']
    Public_repos = r['public_repos']
    Followers = r['followers']
    Following = r['following']
    avatar_url = r['avatar_url']
    #save in User model
    request.user.name = Name
    request.user.bio = Bio
    request.user.location = Location
    request.user.company = Company
    request.user.email = Email
    request.user.public_repos = Public_repos
    request.user.followers = Followers
    request.user.following = Following
    request.user.avatar = avatar_url
    request.user.save()
    return redirect('profile')


@login_required(login_url='/login/')
def profile(request):
    user_profile = User.objects.get(username=request.user.username)
    user_tags = Tags.objects.filter(coder=user_profile)
    invited_teams = user_profile.invites.all()
    user_teams = user_profile.teams.all()
    team_ids=[]
    team_names=[]
    for team in invited_teams:
        team_ids.append(team.id)
        team_names.append(team.name)
    return render(request, 'profile.html', {'user_profile':user_profile, 'team_id':team_ids, 'team_names':team_names, 'user_teams':user_teams, 'user_tags':user_tags})

@login_required(login_url='/login/')

def createteamform(request,username):
    user_profile = User.objects.get(username=username)
    user_tags = Tags.objects.filter(coder=user_profile)
    invited_teams = user_profile.invites.all()
    user_teams = user_profile.teams.all()
    team_ids=[]
    team_names=[]
    for team in invited_teams:
        team_ids.append(team.id)
        team_names.append(team.name)
    if request.method=='POST':
        name = request.POST['teamname']
        description = request.POST['teamdesc']
        print(name, description)
        team=Team(name=name, description=description, teamleader=user_profile)
        team.save()
        team.accepted_members.add(user_profile)
        team.save()
        user_profile.teams.add(team)
        user_profile.save()
        message = "Created team successfully!"
        return render(request, 'profile.html', {'user_profile':user_profile, 'team_id':team_ids, 'team_names':team_names, 'user_teams':user_teams, 'user_tags':user_tags})
    return render(request,'createteamform.html',{'user_profile':user_profile})

@login_required(login_url='/login/')
def createteam(request):
    if request.method == 'POST':
        name = request.POST['teamname']
        description = request.POST['teamdesc']
        print(name, description)
        if Team.objects.filter(name=name).exists():
            message = "Team name already exists!"
            return render(request, 'createteam.html', {'message':message})
        team=Team(name=name, description=description, teamleader=request.user)
        team.save()
        team.accepted_members.add(request.user)
        team.save()
        request.user.teams.add(team)
        request.user.save()
        message = "Created team successfully!"
        return render(request, 'home.html', {'message':message,})
    return render(request, 'createteam.html')


@login_required(login_url='/login/')
def teams(request):
    # Get teams that the user is a part of
    team_list = request.user.teams.all()
    print(team_list)

    combined_list = []  # To store combined data of team, members, and hackathons

    for team in team_list:
        # Fetch the accepted members for each team
        mem_list = [member.username for member in team.accepted_members.all()]

        # Fetch hackathons related to the current team
        hackathons = team.get_hackathons()

        # Append a tuple or dictionary of team, members, and hackathons
        combined_list.append({
            'team': team,
            'members': mem_list,
            'hackathons': hackathons
        })

    return render(request, 'displayteams.html', {
        'combined_list': combined_list,  # Pass the combined list to the template
    })




@login_required(login_url='/login/')
def searchhackathon(request):
    if request.method == 'POST':
         query = request.POST.get('query', '')
         hackathons = Hackathon.objects.filter(Q(name__icontains=query)).distinct()
         return render(request, 'searchhackathon.html', {'hackathons': hackathons})
    return render(request, 'searchhackathon.html')


@login_required(login_url='/login/')
def tags(request):
    if request.method == 'POST':
        tagname = request.POST['tagname']
        u=request.POST['username']
        coder=User.objects.get(username=u)
        tag = Tags(name=tagname, coder=coder)

        tag.save()
    ids = recommend_users(request.user,2)
    
    return render(request, 'tag.html', {'ids':ids})



@login_required(login_url='/login/')
def register_hackathon(request, hack):
    user = request.user
    if request.method == 'POST':
        hackathon = Hackathon.objects.get(name=hack)
        team_name=request.POST['teamname']
        team = Team.objects.get(name=team_name)
        hackathon.teams.add(team)
        hackathon.save()
        return redirect('profile')

    #generate a random dictionary consistings of teams
    h = Hackathon.objects.get(name=hack)
    o = Organization.objects.all()
    org = None
    for i in o:
        if h in i.hackathons.all():
            org = i
    #get organization of the hackathon
    # list_hack=list(h)
    # o = org[0]
    t = h.teams.all().count()
    te =list( h.teams.all())
    tea = list(user.teams.all())
    return render(request, 'uhackathon.html', {'tea':tea, 'h':h,'t':t, 'org':org,'te':te})

@login_required(login_url='/login/')
def register_hackathonform(request, hack):
    hackathon = Hackathon.objects.get(name=hack)
    user = request.user

    if request.method == 'POST':
        team_name = request.POST['teamname']
        team = Team.objects.get(name=team_name)
        # Add team to the hackathon
        hackathon.teams.add(team)
        hackathon.save()
        return redirect('profile')  # Redirect to the profile page after successful registration

    # List the teams of the current user to display in the form
    tea = list(user.teams.all())

    return render(request, 'uhackathonregister.html', {'hackathon': hackathon, 'tea': tea})




def create_hackathon(request,name):
    organization = Organization.objects.get(name=name)
    no_of_hackathons = Organization.objects.get(name=name).hackathons.count()
    hackathons = list(organization.hackathons.all())
    
    print(hackathons)
    return render(request, 'orgyhackathon.html', {'organization':organization, 'no_of_hackathons':no_of_hackathons, 'hackathons':hackathons})

def hackathonform(request, name):
    organization = Organization.objects.get(name=name)
    if request.method == 'POST':
        organization = Organization.objects.get(name=name)
        name = request.POST['hackathonname']
        description = request.POST['hackathondesc']
        print(name, description)
        hackathon = Hackathon(name=name, description=description)
        hackathon.save()
        organization.hackathons.add(hackathon)
        organization.save()
        message = "Created hackathon successfully!"
        hackathons = list(organization.hackathons.all())
        no_of_hackathons=len(hackathons)
        print(hackathons)

        return render(request, 'orgyhackathon.html', {'organization':organization, 'no_of_hackathons':no_of_hackathons, 'hackathons':hackathons})
    return render(request, 'hackathonform.html', {'organization': organization})


@login_required(login_url='/login/')
def addmember(request,id):
    if request.method == 'POST':
        membername = request.POST['username']
        print(membername)
        print(id)
        mem = User.objects.get(username=membername)
        if mem:
            team = Team.objects.get(id=id)
            team.invited_members.add(mem)
            mem.invites.add(team)
            team.save()
            mem.save()
    else:
        message = "User not found"
    return redirect('home')


@login_required(login_url='/login/')
def acceptinvite(request, teamname):
    team = Team.objects.get(name=teamname)
    team.accepted_members.add(request.user)
    team.invited_members.remove(request.user)
    request.user.teams.add(team)
    request.user.invites.remove(team)
    team.save()
    request.user.save()
    return redirect('profile')


@login_required(login_url='/login/')
def rejectinvite(request, teamname):
    team = Team.objects.get(name=teamname)
    team.invited_members.remove(request.user)
    team.save()
    request.user.invites.remove(team)
    request.user.save()
    return redirect('profile')


from django.contrib import messages
from django.contrib.auth import get_user_model  # Import this for custom or default user models
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Tags  # Make sure to import your Tags model if it's in a different app

User = get_user_model()  # This will point to the custom user model if you have one

@login_required(login_url='/login/')
def tags(request):
    if request.method == 'POST':
        tagname = request.POST['tagname']
        u = request.POST['username']

        try:
            # Try to get the user with the provided username
            coder = User.objects.get(username=u)
            # Create and save the tag
            tag = Tags(name=tagname, coder=coder)
            tag.save()
            messages.success(request, f"Tag '{tagname}' added successfully for user '{u}'.")
        except User.DoesNotExist:
            # Handle the case where the user doesn't exist
            messages.error(request, f"User '{u}' does not exist.")
        except Exception as e:
            # Catch any other exceptions
            print(f"Error saving tag: {e}")
            messages.error(request, "An error occurred while saving the tag.")
    
    ids = recommend_users(request.user, 2)
    return render(request, 'tag.html', {'ids': ids})



@login_required(login_url='/login/')
def team(request, id):
    teams = Team.objects.filter(id=id)
    id_list = []
    for team in teams:
        mem_list=[]
        print(team.accepted_members.all())
        for member in team.accepted_members.all():
            if member not in mem_list:
                mem_list.append(member.username)
        id_list.append(mem_list)
    if request.method == 'POST':
        membername = request.POST['username']
        print(membername)
        print(id)
        mem = User.objects.get(username=membername)
        if mem:
            team = Team.objects.get(id=id)
            team.invited_members.add(mem)
            mem.invites.add(team)
            team.save()
            mem.save()
    
    return render(request, 'teamdetails.html', {'team':team,'id_list':id_list})


@login_required(login_url='/login/')
def project(request):
    owner=request.user.username
    if request.method == 'POST':
        repo = request.POST.get('repo')
        owner = request.POST.get('owner')
        print(repo,owner)
        commit_url = f"https://api.github.com/repos/{owner}/{repo}/commits"#issues pulls
        r = requests.get(commit_url)
        i=0
        c_message=r.json()[i]['commit']['message']
        c_date=r.json()[i]['commit']['author']['date']
        c_author=r.json()[i]['commit']['author']['name']
        c_email=r.json()[i]['commit']['author']['email']

        issue_url=f"https://api.github.com/repos/{owner}/{repo}/issues"
        r = requests.get(issue_url)
        issue=r.json()[0]
        body=issue['body']
        issue_created=issue['created_at']
        print(body,issue_created[:10])

        return render(request, 'projects.html',{'c_message':c_message,'c_date':c_date,'c_author':c_author,'c_email':c_email,'body':body,'issue_created':issue_created[:10]})
    return render(request, 'projects.html')