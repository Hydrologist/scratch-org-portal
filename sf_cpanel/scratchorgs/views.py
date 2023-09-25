from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import dateparse, timezone

from .models import Organization, SalesforceUser
from .forms import CreateOrgForm

from . import scratchorgs

# Create your views here.
#@login_required(login_url=reverse_lazy('scratchorgs:login'))
def index(request):
    organization_list = Organization.objects.order_by('-created_date')
    template = loader.get_template('scratchorgs/index.html')
    context = {
        'organization_list': organization_list,
        'form': CreateOrgForm()
    }
    return HttpResponse(template.render(context, request))

#@login_required(login_url=reverse_lazy('scratchorgs:login'))
def user_login(request, user_id):
    if request.method != 'GET':
        return HttpResponse(status=405, headers={'Allow': 'GET'})
    
    user = get_object_or_404(SalesforceUser, pk=user_id)

    result = scratchorgs.get_login_url(user.username)

    login_url = result['result']['url']

    return HttpResponse(login_url, status=200)

#@login_required(login_url=reverse_lazy('scratchorgs:login'))
def generate_password(request, user_id):
    if request.method != 'POST':
        return HttpResponse(status=405, headers={'Allow': 'POST'})
    
    user = get_object_or_404(SalesforceUser, pk=user_id)

    if user.password:
        return HttpResponse(user.password, status=200)
    
    username = user.username

    result = scratchorgs.generate_user_password(username)

    if result['status'] != 0:
        return HttpResponse(result['data'], status=500)
    
    password = result['result']['password']

    user.password = password
    
    user.save()
    
    return HttpResponse(password, status=201)

#@login_required(login_url=reverse_lazy('scratchorgs:login'))
def create_org(request):
    if request.method != 'POST':
        return HttpResponse(status=405, headers={'Allow': 'POST'})
    
    form = CreateOrgForm(request.POST)
    if not form.is_valid():
        return HttpResponse(status=400)
    
    alias = form.cleaned_data['alias']
    result = scratchorgs.create_scratch_org(alias)
    if result['status'] != 0:
        print(result)
        return HttpResponse(result['data'])
    
    username = result['result']['username']

    org_info = result['result']['scratchOrgInfo']
    auth_info = result['result']['authFields']
    expiration_date = timezone.make_aware(dateparse.parse_datetime(org_info['ExpirationDate']))
    namespace = org_info['Namespace'] if org_info['Namespace'] else ''
    
    new_organization = Organization(organization_id=auth_info['orgId'],
                                    instance_url=auth_info['instanceUrl'],
                                    login_url=auth_info['loginUrl'],
                                    access_token=auth_info['accessToken'],
                                    alias=alias,
                                    expiration_date=expiration_date,
                                    namespace=namespace)

    new_organization.save()

    new_user = SalesforceUser(username=username,
                              profile_name='System Administrator',
                              primary_user=True,
                              organization=new_organization)

    new_user.save()

    context = {
        'organization': new_organization
    }

    return HttpResponse(loader.render_to_string('scratchorgs/organization_card.html', context), status=201)

#@login_required(login_url=reverse_lazy('scratchorgs:login'))
def delete_org(request, org_id):
    if request.method != 'POST':
        return HttpResponse(status=405, headers={'Allow': 'POST'})
    
    org = get_object_or_404(Organization, pk=org_id)

    alias = org.alias

    result = scratchorgs.delete_org(alias)

    if result['status'] != 0:
        return JsonResponse(result, status=500)
    
    org.delete()

    return JsonResponse(result, status=200)