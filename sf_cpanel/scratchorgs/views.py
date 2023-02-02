from django.shortcuts import render
from django.http import HttpResponse

from . import scratchorgs

# Create your views here.
def index(request):
    return HttpResponse(scratchorgs.sfdx_test())
