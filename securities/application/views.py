from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ApplicationForm
from .repository import Repository


@login_required(login_url='/accounts/login/')
def apply_view(request):
    repo = Repository()
    existing_app = repo.get_application_by_user(request.user)

    if existing_app:
        # this user has previous unfinished application, redirect to the status page of the application
        return redirect('application_status')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        repo.save_application_and_update_status(form, request.user, 'PENDING')
        messages.success(request, "The application has been submitted. Please wait for reviewing.")
        return redirect('application_status')
    else:
        # GET case return an empty form
        form = ApplicationForm()
    return render(request, 'apply.html', {'form': form})


@login_required(login_url='/accounts/login/')
def status_view(request):
    repo = Repository()
    app = repo.get_application_by_user(request.user, raise_404_if_not_exist=True)
    context = {'application': app}

    if app.status == 'PENDING':
        messages.success(request, 'Your application is currently under review.')
    elif app.status == 'APPROVED':
        messages.success(request, 'Congratulation! Your application has been approved.')
    elif app.status == 'REJECTED':
        messages.info(request, f'The application has been rejected. Reason: {app.reason}')
    elif app.status == 'MISSING_DOCUMENTS':
        messages.info(request, f'The application is missing some necessary information. Reason: {app.reason}')
    return render(request, 'status.html', context)


@login_required
def update_application_view(request):
    repo = Repository()
    app = repo.get_application_by_user(request.user, status='MISSING_DOCUMENTS', raise_404_if_not_exist=True)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=app)
        repo.save_application_and_update_status(form, request.user, 'PENDING')
        messages.success(request, "The application has been submitted. Please wait for reviewing.")
        return redirect('application_status')
    else:
        # GET case return the empty application form
        form = ApplicationForm(instance=app)
    return render(request, 'update_application.html', {'form': form})