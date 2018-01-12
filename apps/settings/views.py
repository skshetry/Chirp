from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def settings_view(request):
    """The Settings page view."""
    return render(request, 'settings.html')
