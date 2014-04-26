from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from users.forms import UserForm, NewUser, LoginForm, FileForm, Del_Video, Del_File, Del_Photo
from users.models import UserProfile, UserFile

def index(request):
    new_user = NewUser()
    language = 'en-gb'
    session_language = 'en-gb'
    if 'lang' in request.COOKIES:
        language = request.COOKIES['lang']
    if 'lang' in request.session:
        session_language = request.session['lang']
    all_users = User.objects.all()
    if request.method == 'POST':
        new_user = NewUser(request.POST)
        if new_user.is_valid():
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password = request.POST['password']
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
        else:
            new_user = NewUser()
    context = {'all_users': all_users, 'language': language, 'session_lang': session_language, 'new_user': new_user}
    return render(request, 'users/index.html', context)

def detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    userprofile = get_object_or_404(UserProfile, user=user)
    year = datetime.now().year
    file = UserFile.objects.get(file='image.txt')
    userform = UserForm(initial={'description': userprofile.description})
    fileform = FileForm(initial={'profile': userprofile})
    delvid = Del_Video()
    delphoto = Del_Photo()
    delfile = Del_File()
    if request.method == 'POST':
        userform = UserForm(request.POST, request.FILES, instance=user)
        delvid = Del_Video(request.POST)
        delfile = Del_File(request.POST)
        delphoto = Del_Photo(request.POST)
        fileform = FileForm(request.POST, request.FILES)
        if userform.is_valid():
            userprofile.description = request.POST.get('description', userprofile.description)
            userprofile.photo = request.FILES.get('photo', userprofile.photo)
            userprofile.video = request.FILES.get('video', userprofile.video)
            userprofile.rand_file = request.FILES.get('rand_file', userprofile.rand_file)
            userprofile.save()
        else:
            messages.add_message(request, messages.INFO, userform.errors)
            userform = UserForm()
        if delvid.is_valid():
            if request.POST['Delete']:
                userprofile.video.delete()
        else:
            delvid = Del_Video()
        if delphoto.is_valid():
            if request.POST['Delete']:
                userprofile.photo.delete()
        else:
            delphoto = Del_Photo()
        if delfile.is_valid():
            if request.POST['Delete']:
                userprofile.rand_file.delete()
        else:
            delfile = Del_File()
        if fileform.is_valid():
            fileform.save()
        else:
            fileform = FileForm()
    context = {'user': user, 'year': year, 'userform': userform, 'userprofile': userprofile, 'delvid': delvid,
               'delfile': delfile, 'delphoto': delphoto, 'fileform': fileform, 'file': file}
    return render(request, 'users/detail.html', context)

def download_img(request, photo):
    photo = get_object_or_404(User, photo=photo)
    fsock = open(photo.name, 'r')
    response = HttpResponse(fsock, mimetype='image/jpeg')
    response['Content-Disposition'] = "attachment; filename=%s" % photo.name
    return response

def language(request, language='en-gb'):
    response = HttpResponse('setting language to %s' % language)
    response.set_cookie('lang', language)
    request.session['lang'] = language
    return response

def user_login(request):
    loginform = LoginForm()
    invalid = ''
    disabled = ''
    if request.method == 'POST':
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('users:u_success', args=(user.id,)))
                else:
                    disabled = 'User is not active'
                    context = {'loginform': loginform, 'invalid': invalid, 'disabled': disabled}
                    return render(request, 'users/login.html', context)
            else:
                invalid = 'User credentials invalid'
                context = {'loginform': loginform, 'invalid': invalid, 'disabled': disabled}
                return render(request, 'users/login.html', context)
    else:
        loginform = LoginForm()
        context = {'loginform': loginform, 'invalid': invalid, 'disabled': disabled}
        return render(request, 'users/login.html', context)

def user_login_success(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    prof = get_object_or_404(UserProfile, user=user)
    context = {'user': user, 'prof': prof}
    return render(request, 'users/success.html', context)

def user_logout(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'You have been successfully logged out.')
    return HttpResponseRedirect(reverse('users:index'))
