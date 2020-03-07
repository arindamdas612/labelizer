from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UpdateProfileForm

@login_required
def profile(request):
    template_name = 'profile.html'
    form = UpdateProfileForm()
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        form = UpdateProfileForm(data=request.POST,u=request.user.username, e=request.user.email)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('firstname')
            user.last_name = form.cleaned_data.get('lastname')
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Your profile was updated.')
    context = {}
    form.fields["firstname"].initial = request.user.first_name
    form.fields["lastname"].initial = request.user.last_name
    form.fields["username"].initial = request.user.username
    form.fields["email"].initial = request.user.email
    context['form'] = form
    context['title'] = 'My Profile'
    context['avatar_path'] = "img/avatars/" + user.userprofile.avatar_name + ".jpg"
    return render(request, template_name, context=context)

@login_required
def update_password(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        
        curr_password = request.POST.get('password_current')
        new_password = request.POST.get('password')
        cnf_password = request.POST.get('password1')

        if user.check_password(curr_password) and new_password == cnf_password:
            user.set_password(cnf_password)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Password was updated.')
        elif not user.check_password(curr_password):
            messages.add_message(request, messages.WARNING, 'Invalid Password.')
        else:
            messages.add_message(request, messages.WARNING, 'Passwords do not match.')
    return redirect('my_profile')


@login_required
def update_avatar(request):
    if request.method == 'POST':
        avatar_name = request.POST.get('profile_avatar')
        if len(avatar_name) > 0:
            user = User.objects.get(id=request.user.id)
            user.userprofile.avatar_name = avatar_name
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Profile avatar changed.')
    return redirect('my_profile')

