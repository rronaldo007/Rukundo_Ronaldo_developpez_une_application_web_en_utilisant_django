#!/usr/bin/env python
"""Script pour créer des données de test pour LITReview."""

import os
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from reviews.models import Ticket, Review, UserFollows


def create_test_data():
    """Crée des utilisateurs, tickets et reviews de test."""
    
    print("Création des données de test...")
    
    # Créer des utilisateurs
    users_data = [
        {'username': 'jean_5679', 'password': 'testpass123'},
        {'username': 'sarahj', 'password': 'testpass123'},
        {'username': 'severine123', 'password': 'testpass123'},
        {'username': 'admin', 'password': 'admin123', 'is_superuser': True, 'is_staff': True},
    ]
    
    users = {}
    for user_data in users_data:
        username = user_data.pop('username')
        password = user_data.pop('password')
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults=user_data
        )
        if created:
            user.set_password(password)
            user.save()
            print(f"  Utilisateur créé: {username}")
        else:
            print(f"  Utilisateur existant: {username}")
        users[username] = user
    
    # Créer des tickets
    tickets_data = [
        {
            'title': 'The Origin of Species - Charles Darwin',
            'description': 'Je suis à la recherche d\'un avis sur ce sujet, svp, merci !',
            'user': users['jean_5679'],
        },
        {
            'title': 'Une brève histoire du temps - Stephen Hawking',
            'description': '',
            'user': users['sarahj'],
        },
        {
            'title': 'Discours de la méthode - René Descartes',
            'description': 'Un classique de la philosophie !',
            'user': users['sarahj'],
        },
        {
            'title': 'La relativité - Albert Einstein',
            'description': 'Qui peut m\'expliquer cette théorie ?',
            'user': users['severine123'],
        },
    ]
    
    tickets = []
    for ticket_data in tickets_data:
        ticket, created = Ticket.objects.get_or_create(
            title=ticket_data['title'],
            user=ticket_data['user'],
            defaults={'description': ticket_data['description']}
        )
        if created:
            print(f"  Ticket créé: {ticket.title}")
        tickets.append(ticket)
    
    # Créer des reviews
    reviews_data = [
        {
            'ticket': tickets[0],
            'headline': 'Véritablement révolutionnaire',
            'body': 'Une excellente lecture et je vous recommande vivement !',
            'rating': 5,
            'user': users['sarahj'],
        },
        {
            'ticket': tickets[2],
            'headline': 'Excellent',
            'body': 'Un must-read pour tout amateur de philosophie.',
            'rating': 4,
            'user': users['severine123'],
        },
        {
            'ticket': tickets[3],
            'headline': 'Exceptionnel',
            'body': 'Einstein explique de manière accessible une théorie complexe.',
            'rating': 5,
            'user': users['severine123'],
        },
    ]
    
    for review_data in reviews_data:
        review, created = Review.objects.get_or_create(
            ticket=review_data['ticket'],
            user=review_data['user'],
            defaults={
                'headline': review_data['headline'],
                'body': review_data['body'],
                'rating': review_data['rating'],
            }
        )
        if created:
            print(f"  Review créée: {review.headline}")
    
    # Créer des abonnements
    follows_data = [
        {'user': users['jean_5679'], 'followed_user': users['sarahj']},
        {'user': users['jean_5679'], 'followed_user': users['severine123']},
        {'user': users['sarahj'], 'followed_user': users['jean_5679']},
        {'user': users['severine123'], 'followed_user': users['jean_5679']},
    ]
    
    for follow_data in follows_data:
        follow, created = UserFollows.objects.get_or_create(**follow_data)
        if created:
            print(f"  Abonnement créé: {follow.user.username} -> {follow.followed_user.username}")
    
    print("\nDonnées de test créées avec succès !")
    print("\nComptes disponibles:")
    print("  - admin / admin123 (superutilisateur)")
    print("  - jean_5679 / testpass123")
    print("  - sarahj / testpass123")
    print("  - severine123 / testpass123")


if __name__ == '__main__':
    create_test_data()
