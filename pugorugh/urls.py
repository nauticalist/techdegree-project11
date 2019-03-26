from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from pugorugh.views import (UserRegisterView, RetrieveDogView, UpdateDogView,
                            RetrieveUpdateUserPrefView, DogProfileViewSet)

app_name = 'pugorugh'


urlpatterns = format_suffix_patterns([
    url(r'^api/user/login/$', obtain_auth_token, name='login-user'),
    url(r'^api/user/$', UserRegisterView.as_view(), name='register-user'),
    url(r'^favicon\.ico$',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^api/dog/(?P<pk>-?\d+)/(?P<status>liked|disliked|undecided)/next/$',
        RetrieveDogView.as_view(),
        name='next-dog'),
    url(r'^api/dog/(?P<pk>-?\d+)/(?P<status>liked|disliked|undecided)/$',
        UpdateDogView.as_view(),
        name='update-dog'),
    url(r'^api/user/preferences/$',
        RetrieveUpdateUserPrefView.as_view(),
        name='user-preferences'),

])

urlpatterns += [
    url(r'^api/dogs$',
        DogProfileViewSet.as_view(
            {"get": "list", "post": "create",}),
        name='dogs',
    ),
    url(r'^api/dogs/(?P<pk>-?\d+)/$', 
        DogProfileViewSet.as_view(
            {"get": "retrieve", 
             "post": "create", 
             "put": "update", 
             "patch": "partial_update", 
             "delete": "destroy"}),
        name="dog-detail"),
]