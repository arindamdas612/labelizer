from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.db.models import Q

from django.views.generic.list import ListView

from django.contrib import messages

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from django.contrib.auth.models import User

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from .forms import AddStaffForm

@staff_member_required(login_url='/accounts/login')
@login_required
def staff(request):
    paginate_by = 10
    form = AddStaffForm(request.POST or None)
    template_name = 'staff.html'
    context = {}
    if request.method == 'POST':
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data.get('username'), password='111111', email=form.cleaned_data.get('email'), is_active=False)
            form = AddStaffForm()
            messages.add_message(request, messages.SUCCESS, 'New Staff added.')
    list_user = User.objects.filter(~Q(pk=request.user.id)).order_by('-id')
    paginator = Paginator(list_user, paginate_by)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    add_form = AddStaffForm()
    context['list_users'] = users
    context['form'] = form
    context['title'] = 'Staffs'
    context['avatar_path'] = "img/avatars/" + request.user.userprofile.avatar_name + ".jpg"
    return render(request, template_name, context=context)


@staff_member_required(login_url='/accounts/login')
@login_required
def change_status(request, staff_id):
    staff = User.objects.get(id=staff_id)
    staff.is_active = not staff.is_active
    staff.save()
    if staff.is_active:
        messages.add_message(
            request, messages.INFO, 
            f'Staff {staff.username}, Activated. The staf will be able to log into the System.'
        )
    else:
        messages.add_message(
            request, 
            messages.INFO, 
            f'Staff {staff.username} Deactivated. The staff will not be able to log in to the system until Activated.')
    return redirect('all_staff')


@staff_member_required(login_url='/accounts/login')
@login_required
def change_role(request, staff_id):
    staff = User.objects.get(id=staff_id)
    staff.is_staff = not staff.is_staff
    staff.save()
    if staff.is_staff:
        messages.add_message(
            request, 
            messages.WARNING, 
            f'Role of staff {staff.username} changed to ADMIN. The staff can now be able to control all other staffs including you.'
        )
    else:
        messages.add_message(
            request, messages.INFO, 
            f'Role of staff {staff.username} changed to STAFF. Staff permissions detained.'
        )
    return redirect('all_staff')


@staff_member_required(login_url='/accounts/login')
@login_required
def delete_staff(request, staff_id):
    staff = User.objects.get(id=staff_id)
    username = staff.username
    messages.add_message(
            request, messages.WARNING, 
            f'Staff {username} deleted.'
        )
    staff.delete()
    return redirect('all_staff')


@staff_member_required(login_url='/accounts/login')
@login_required
def reset_password(request, staff_id):
    staff = User.objects.get(id=staff_id)
    staff.set_password('111111')
    messages.add_message(
        request, messages.SUCCESS, 
        f'Password resest for Staff {staff.username} successful.'
    )
    staff.save()
    return redirect('all_staff')