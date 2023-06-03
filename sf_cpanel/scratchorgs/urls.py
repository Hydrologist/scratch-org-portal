from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    # ex. /scratchorgs
    path('', views.index, name='index'),
    # ex. /scratchorgs/5
    #path('<int:org_id>/', views.org_detail, name='org-detail'),
    # ex: /scratchorgs/5/delete
    path('<int:org_id>/delete/', views.delete_org, name='delete-org'),
    # ex: /scratchorgs/create
    path('create/', views.create_org, name='create-org'),
    # ex: /scratchorgs/users/1/generate
    path('users/<int:user_id>/generate/', views.generate_password, name='generate-password'),
    # ex: /scratchorgs/users/1/login
    path('users/<int:user_id>/login/', views.user_login, name='user-login'),
    # ex: /scratchorg/login
    path('login/', auth_views.LoginView.as_view(template_name='scratchorgs/login.html', next_page=reverse_lazy('scratchorgs:index')), name='login'),
    # ex: /scratchorg/logout
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('scratchorgs:login')), name='logout')
]
