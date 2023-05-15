from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Organization, SalesforceUser
from .forms import CreateOrgForm

from . import scratchorgs

# Create your views here.
def index(request):
    organization_list = Organization.objects.order_by('-created_date')
    template = loader.get_template('scratchorgs/index.html')
    context = {
        'organization_list': organization_list,
        'form': CreateOrgForm()
    }
    return HttpResponse(template.render(context, request))

def org_list(request):
    if request.method != 'GET':
        return HttpResponse(status=405, headers={'Allow': 'GET'})
    
    return HttpResponse(scratchorgs.get_org_list())        

def create_org(request):
    try:
        if request.method != 'POST':
            return HttpResponse(status=405, headers={'Allow': 'POST'})
        
        form = CreateOrgForm(request.POST)
        if not form.is_valid():
            return HttpResponse(status=400)
        
        alias = form.cleaned_data['alias']
        scratch_org_username = scratchorgs.create_scratch_org(alias)
        return HttpResponse(scratch_org_username, status=201);
    except Exception as e:
        return HttpResponse(status=500)