# apps/pages/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


# Link 'pages' app urls to views
urlpatterns = [

    # Homepage
    path(
        '',
        views.HomePageView.as_view(),
        name='home'
    ),

    # Add/View/Edit Trips
    path(
        'trips/',
        views.TripPageView.as_view(),
        name='trip_list'
    ),
    path(
        'trips/add/',
        views.TripCreateView.as_view(),
        name='trip_create'
    ),
    path('trips/<int:pk>/edit',
         views.TripUpdateView.as_view(),
         name='trip_edit'
         ),
    path('trips/<int:pk>/delete',
         views.TripDeleteView.as_view(),
         name='trip_delete'
         ),

    # Password Reset
    path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'password_reset_confirm/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
]
