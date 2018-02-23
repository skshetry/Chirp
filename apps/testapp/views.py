import logging
import os

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Images, ImageUploadForm

logger=logging.getLogger('raven')

# Create your views here.
@login_required
def test_view(request):
    send_mail('Subject here','Here is the message.','from@example.com',[os.environ.get('DJANGO_ADMINS_EMAIL_ADDRESS',default='acb@pahcjsdjsdkskssdskdskdjskdjsdsdskdjskdksjkdksexample.com')],fail_silently=False,)
    #email failing?
    logger.error("Error occured.")
    return render(request, 'a.html')

@login_required
def upload_view(request):
    all_images = all_images = Images.objects.all()
    if request.method == 'GET':
        imageuploadform = ImageUploadForm()
    elif request.method == 'POST':
        imageuploadform = ImageUploadForm(request.POST, request.FILES)
        if imageuploadform.is_valid:
            imageuploadform.save()
    return render(request, 'b.html', {'form':imageuploadform, 'all_images':all_images})


class TestView(TemplateView):
    template_name = 'base.html'
