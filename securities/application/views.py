from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Application
from .forms import ApplicationForm


@login_required(login_url='/accounts/login/')
def apply_view(request):
    existing_app = Application.objects.filter(user=request.user).first()
    if existing_app:
        return redirect('application_status')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.save()
            messages.success(request, "The application has been submitted. Please wait for reviewing.")
            return redirect('application_status')
    else:
        form = ApplicationForm()
    return render(request, 'apply.html', {'form': form})


@login_required(login_url='/accounts/login/')
def application_status_view(request):
    app = get_object_or_404(Application, user=request.user)
    context = {'application': app}

    print("app.status:", app.status)
    if app.status == 'PENDING':
        messages.success(request, "Your application is currently under review.")
    elif app.status == 'APPROVED':
        messages.success(request, "Congratulation! Your application has been approved.")
    elif app.status == 'REJECTED':
        messages.info(request, f"The application has been rejected. Reason: {app.reason}")
    elif app.status == 'MISSING_DOCUMENTS':
        messages.info(request, f"The application is missing some necessary information. Reason: {app.reason}")
    return render(request, 'status.html', context)


@login_required
def update_application_view(request):
    app = get_object_or_404(Application, user=request.user, status='MISSING_DOCUMENTS')
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=app)
        if form.is_valid():
            form.save()
            app.status = 'PENDING'
            app.save()
            messages.success(request, "The application has been submitted. Please wait for reviewing.")
            return redirect('application_status')
    else:
        form = ApplicationForm(instance=app)
    return render(request, 'update_application.html', {'form': form})