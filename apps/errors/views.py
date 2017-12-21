"""This contains views for the possible errors that could occur."""

from django.shortcuts import render


def server_error(request):
    """View for Internal Server Errors."""
    return render(request, '500.html', status=500)


def not_found(request):
    """View if no page/resource is found."""
    return render(request, '404.html', status=404)


def permission_denied(request):
    """View in case user requests for inaccesible item."""
    return render(request, '403.html', status=403)


def bad_request(request):
    """View for bad requests."""
    return render(request, '400.html', status=400)
