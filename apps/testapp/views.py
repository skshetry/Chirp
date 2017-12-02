from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
import os

# Create your views here.
def test_view(request):
    send_mail(
        'Subject here',
        'Here is the message.',
        'from@example.com',
        [os.environ.get('DJANGO_ADMINS_EMAIL_ADDRESS',default='acb@pahcjsdjsdkskssdskdskdjskdjsdsdskdjskdksjkdksexample.com')],
        fail_silently=False,
    )
    return render(request, 'a.html')