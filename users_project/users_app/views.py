from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse

from users_app.forms import UserForm, UserProfileInfoForm
from users_app.models import UserProfileInfo


def index(request):

    return render(request, 'users_app/index.html')


@login_required
def user_logged_in(request):

    return HttpResponse('You are logged in!')


@login_required
def user_logout(request):

    logout(request)
    return redirect('index')


def register(request):

    user_form = UserForm()
    profile_form = UserProfileInfoForm()

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:

                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

        else:

            print(user_form.errors, profile_form.errors)

    return render(request, 'users_app/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if not user:

            print("Unknown user tried to login: username={}, password={}".format(
                username, password))
            return render(request, 'users_app/login.html', {'error_message': 'Incorrect credentials!'})

        if user and user.is_active:

            login(request, user)
            return redirect('index')

    return render(request, 'users_app/login.html', {})
