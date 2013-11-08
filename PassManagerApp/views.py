# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from PassManagerApp.forms import *
from PassManagerApp.models import *

def main_page(request):
#renders the main page
    return render_to_response(
                              'main_page.html',
                              RequestContext(request)
                              )
@login_required
def user_page(request, username):
    #checking if user is viewing his own account
    if request.user.username != username:
        raise Http404(u'You cannot access logins from another user!')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404(u'Requested user not found.')
    #saves the logins for the user and renders the user page
    logins = user.login_set.all()
    template = get_template('user_page.html')
    variables = RequestContext(request, {
                               'username': username,
                               'logins': logins
                               })
    return render_to_response('user_page.html', variables)
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
def register_page(request):
    #if we access this from post method, means that the user has already submitted his registration details. If not, we load the default registration form
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        #checking the form values if are valid
        if form.is_valid():
            #create a new user if all validations have passed
            user = User.objects.create_user(
                                            username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'],
                                            email=form.cleaned_data['email']
                                            )
            UserProfile.first_name=form.cleaned_data['first_name']
            created = UserProfile.objects.get_or_create(
                                                        user_id=user.id, first_name=form.cleaned_data['first_name'], last_name=form.cleaned_data['last_name']    )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
                               'form': form
                               })
    return render_to_response(
                              'registration/register.html', variables)
@login_required
def login_save_page(request):
    #if we access this from post method, means that the user has already submitted the save request. If not, we load the default savelogin form
    if request.method == 'POST':
        form = LoginSaveForm(request.POST)
        #checking form for errors
        if form.is_valid():
            # create or get login.
            login1 = _login_save(request, form)
            return HttpResponseRedirect(
                                        '/user/%s/' % request.user.username
                                        )
    else:
        form = LoginSaveForm()
    variables = RequestContext(request, {
                               'form': form
                               })
    return render_to_response('login_save_page.html', variables)
@login_required
def login_edit_page(request):
    #if we access this from post method, means that the user has already submitted the edit request. If not, we load the default editlogin form
    #saving the login entry id to a new variable
    id2 = request.GET.get('id', None)
    if request.method == 'POST':
        form = LoginEditForm(request.POST)
        #checking form for errors
        if form.is_valid():
            login1 = _login_edit(request, form)
            return HttpResponseRedirect(
                                        '/user/%s/' % request.user.username
                                        )
    #below excecutes if we not access the page from method post. We load a new edit form
    name=''
    url=''
    Login_username =''
    notes= ''
    password=''
    try:
        login1 = login.objects.get(
                                   id = id2
                                  )
        #checking if user views his own logins
        if request.user == login1.username:
            name = login1.name
            url = login1.loginUrl
            Login_username = login1.login_username
            notes = login1.notes
            password = login1.password
        else:
             raise Http404(u'You cannot edit logins from another user!')
    except (login.DoesNotExist):
        pass
    #recovers the stored data for the requested login
    form = LoginEditForm({
                          'name': name,
                          'url': url,
                          'Login_username': Login_username,
                          'notes': notes,
                          'password': password,
                          'id':id2
                        })
    variables = RequestContext(request, {
                                        'form': form
                                        })
    login1 = _login_edit(request, form)
    ctx = {
            'form': form,
            'id': request.GET.get('id', None)
          }
    return render_to_response('login_edit_page.html', ctx,
                              context_instance=RequestContext(request))
@login_required
def login_delete_page(request):
    #set the login1 to the login obgect we want to delete
    login1, created = login.objects.get_or_create(
                                                  id=request.GET.get('id', None)
                                                  )
    #perfoming delete request and redirecting to user page
    login1.delete()
    return HttpResponseRedirect(
                                '/user/%s/' % request.user.username
                                )
@login_required
def _login_save(request, form):
    #implements the login save process
    #ensuring that we access it from post method
    if request.method == 'POST':
        #saving the form from LoginSaveForm
        form = LoginSaveForm(request.POST)
        if form.is_valid():
            #checking if form is valid and creating a new login with the username of the connected user
            login1 = login.objects.create(
                                          username=request.user
                                         )
            login1.name=form.cleaned_data['name']
            login1.loginUrl = form.cleaned_data['url']
            login1.password = form.cleaned_data['password']
            login1.login_username = form.cleaned_data['Login_username']
            login1.notes = form.cleaned_data['notes']
            login1.save()
    return login1
def _login_edit(request, form):
    #implements the login edit process
    #ensuring that we access it from post method
    if request.method == 'POST':
        form = LoginEditForm(request.POST)
        if form.is_valid():
            #checking if form is valid and asking to update the login entry of the connected user
            login1, created = login.objects.get_or_create(
                                       id=form.cleaned_data['id']
                                       )
            login1.name=form.cleaned_data['name']
            login1.loginUrl = form.cleaned_data['url']
            login1.password = form.cleaned_data['password']
            login1.login_username = form.cleaned_data['Login_username']
            login1.notes = form.cleaned_data['notes']
            login1.save()
        return login1