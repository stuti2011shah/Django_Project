from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from base.models import Organization

# Create your views here.
def login(request):
    return render(request, 'login.html')

def logoutv(request):
    logout(request)
    return redirect('login')


def registerOrg(request):
    if request.method == 'POST':
        # Get the form values
        orgName = request.POST.get('orgName', '').strip()
        orgEmail = request.POST.get('orgEmail', '').strip()
        orgLoc = request.POST.get('orgLoc', '').strip()
        orgPass = request.POST.get('orgPass', '').strip()
        orgDesc = request.POST.get('orgDesc', '').strip()
        orgPassConfirm = request.POST.get('orgPassConfirm', '').strip()
        orgImage = request.FILES.get('orgImage')

        # Check if all required fields are filled
        if not orgName:
            messages.error(request, 'Organization Name is required.')
            return redirect('registerOrg')
        if not orgEmail:
            messages.error(request, 'Organization Email is required.')
            return redirect('registerOrg')
        if not orgLoc:
            messages.error(request, 'Organization Location is required.')
            return redirect('registerOrg')
        if not orgPass or not orgPassConfirm:
            messages.error(request, 'Password and confirmation are required.')
            return redirect('registerOrg')
        if orgPass != orgPassConfirm:
            messages.error(request, 'Passwords do not match.')
            return redirect('registerOrg')
        if not orgImage:
            messages.error(request, 'Organization Image is required.')
            return redirect('registerOrg')

        # Check if the email is already registered
        if Organization.objects.filter(email=orgEmail).exists():
            messages.error(request, 'Email already exists.')
            return redirect('registerOrg')
        else:
            # Create and save the new organization
            organization = Organization.objects.create(
                name=orgName, description=orgDesc, email=orgEmail,
                location=orgLoc, password=orgPass, image=orgImage
            )
            organization.save()

            # Redirect to the login page after successful registration
            messages.success(request, 'Organization registered successfully!')
            return redirect('loginOrg')

    return render(request, 'registerOrg.html')


def loginOrg(request):
    if request.method=='POST':
        orgEmail = request.POST['orgEmail']
        orgPass= request.POST['orgPass']
        if Organization.objects.filter(email=orgEmail).exists():
            organization = Organization.objects.get(email=orgEmail)
            if organization.password==orgPass:
                return redirect("organization", organization.name)
            else:
                messages.info(request, 'Invalid Password')
                return redirect('loginOrg')
        else:
            messages.info(request, 'Invalid Email')
            return redirect('loginOrg')
    return render(request, 'loginOrg.html')