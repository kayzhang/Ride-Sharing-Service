from django.urls import path
from .views import (
            RideListView,
            RideDetailView,
            RideCreateView,
            RideUpdateView,
            RideDeleteView,
            OwnerRideListView,
            ShareCreateView,
            SharePickRideListView,
            ShareRideListView,
            DriverListView,
            ShareUpdateView
            )
from . import views
from .models import Ride, Share
from django.contrib.auth import views as auth_views

app_name = 'ride'
urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='users/login.html')),
    path('home/', views.home, name='ride-home'),
    # path('about/', views.about, name='ride-about'),
    path('owner/', views.owner, name='owner-home'),
    path('sharer/', views.sharer, name='sharer-home'),
    path('driver/', views.driver, name='driver-home'),
    path('owner/request/', RideCreateView.as_view(), name='owner-request'),
    path('driver/request/', DriverListView.as_view(), name='driver-request'),
    path('owner/view/', OwnerRideListView.as_view(), name='owner-view'),
    path('ride/<int:pk>/', RideDetailView.as_view(), name='ride-detail'),
    path('owner/view/<int:pk>/update/', RideUpdateView.as_view(), name='owner-update'),
    path('owner/view/<int:pk>/delete/', RideDeleteView.as_view(), name='owner-delete'),
    path('driver/<int:ride_id>/confirm/', views.driver_confirm, name='driver-confirm'),
    path('driver/<int:ride_id>/complete/', views.driver_complete, name='driver-complete'),
    path('sharer/request/', ShareCreateView.as_view(), name='share-request'),
    path('sharer/list/', SharePickRideListView.as_view(), name='share-list'),
    path('sharer/<int:ride_id>/join/', views.share_join, name='share-join'),
    path('sharer/<int:ride_id>/cancel/', views.share_cancel, name='share-cancel'),
    # path('sharer/view/', ShareRideListView.as_view(), name='share-view'),
    path('sharer/view/', views.share_view, name='share-view'),
    path('sharer/<int:pk>/update/', ShareUpdateView.as_view(), name='share-update'),
    path('driver/view/', views.driver_view, name='driver-view'),
]
