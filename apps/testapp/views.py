from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404
import logging
import os
from .models import Images, ImageUploadForm

logger=logging.getLogger('raven')

# Create your views here.
def test_view(request):
    send_mail('Subject here','Here is the message.','from@example.com',[os.environ.get('DJANGO_ADMINS_EMAIL_ADDRESS',default='acb@pahcjsdjsdkskssdskdskdjskdjsdsdskdjskdksjkdksexample.com')],fail_silently=False,)
    #email failing?
    logger.error("Error occured.")
    try:
        return render(request, 'a.html')
    except request.DoesNotExist:
        raise Http404('Page not found')

def upload_view(request):
    all_images = all_images = Images.objects.all()
    if request.method == 'GET':
        imageuploadform = ImageUploadForm()
    elif request.method == 'POST':
        imageuploadform = ImageUploadForm(request.POST, request.FILES)
        if imageuploadform.is_valid:
            imageuploadform.save()
    return render(request, 'b.html', {'form':imageuploadform, 'all_images':all_images})
