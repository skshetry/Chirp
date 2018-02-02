import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from apps.posts.models import Post
from apps.decorators import ajax_required
# Create your views here.
