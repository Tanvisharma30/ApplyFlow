
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import ApplicationForm, SignupForm, UserProfileForm
from .models import Application, UserProfile

User = get_user_model()


def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()

            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'name': user.username,
                    'email': user.email,
                },
            )

            login(request, user)
            messages.success(
                request,
                'Your ApplyFlow account has been created.'
            )
            return redirect('dashboard')
    else:
        form = SignupForm()

    return render(request, 'applications/signup.html', {
        'form': form
    })


@login_required
def dashboard(request):
    all_applications = Application.objects.filter(user=request.user)
    applications = all_applications.order_by('-applied_on')

    query = request.GET.get('q', '').strip()
    selected_status = request.GET.get('status', '').strip()

    if query:
        applications = applications.filter(
            Q(company__icontains=query)
            | Q(role__icontains=query)
            | Q(location__icontains=query)
        )

    valid_statuses = [
        choice[0] for choice in Application.STATUS_CHOICES
    ]

    if selected_status in valid_statuses:
        applications = applications.filter(status=selected_status)

    context = {
        'applications': applications,
        'total': all_applications.count(),
        'applied': all_applications.filter(status='Applied').count(),
        'shortlisted': all_applications.filter(
            status='Shortlisted'
        ).count(),
        'interviews': all_applications.filter(
            status='Interview'
        ).count(),
        'offers': all_applications.filter(status='Offer').count(),
        'query': query,
        'selected_status': selected_status,
        'status_choices': Application.STATUS_CHOICES,
    }

    return render(
        request,
        'applications/dashboard.html',
        context
    )


@login_required
def add_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()

            messages.success(
                request,
                'Application added successfully!'
            )
            return redirect('dashboard')
    else:
        form = ApplicationForm()

    return render(request, 'applications/add_application.html', {
        'form': form
    })


@login_required
def edit_application(request, pk):
    application = get_object_or_404(
        Application,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        form = ApplicationForm(
            request.POST,
            instance=application
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Application updated successfully!'
            )
            return redirect('dashboard')
    else:
        form = ApplicationForm(instance=application)

    return render(request, 'applications/edit_application.html', {
        'form': form,
        'application': application
    })


@login_required
@require_POST
def delete_application(request, pk):
    application = get_object_or_404(
        Application,
        pk=pk,
        user=request.user
    )
    application.delete()

    messages.success(
        request,
        'Application deleted successfully!'
    )
    return redirect('dashboard')


@login_required
def profile(request):
    profile_obj, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'name': request.user.get_full_name()
            or request.user.username,
            'email': request.user.email,
        },
    )

    if request.method == 'POST':
        form = UserProfileForm(
            request.POST,
            instance=profile_obj
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your profile has been updated.'
            )
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile_obj)

    return render(request, 'applications/profile.html', {
        'form': form,
        'profile': profile_obj,
    })
