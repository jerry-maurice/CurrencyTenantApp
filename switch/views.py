from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.shortcuts import redirect

import logging

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    return HttpResponse("you are in the homepage")
