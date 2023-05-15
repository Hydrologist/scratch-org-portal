from django.urls import path

from . import views

urlpatterns = [
    # ex. /scratchorgs
    path('', views.index, name='index'),
    # ex. /scratchorgs/5
    #path('<int:org_id>/', views.org_detail, name='org-detail'),
    # ex: /scratchorgs/5/delete
    #path('<int:org_id>/delete/', views.delete_org, name='delete-org'),
    # ex: /scratchorgs/create
    path('create/', views.create_org, name='create-org')
]
