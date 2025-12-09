from django.urls import path
from . import views

urlpatterns = [
    # Authentification
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # Flux
    path('feed/', views.feed, name='feed'),
    
    # Tickets
    path('ticket/create/', views.create_ticket, name='create_ticket'),
    path('ticket/<int:ticket_id>/edit/', views.edit_ticket, name='edit_ticket'),
    path('ticket/<int:ticket_id>/delete/', views.delete_ticket, name='delete_ticket'),
    
    # Critiques
    path('review/create/<int:ticket_id>/', views.create_review, name='create_review'),
    path('review/create/', views.create_review_standalone, name='create_review_standalone'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    
    # Posts de l'utilisateur
    path('posts/', views.posts, name='posts'),
    
    # Abonnements
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('unfollow/<int:user_id>/', views.unfollow, name='unfollow'),
]
