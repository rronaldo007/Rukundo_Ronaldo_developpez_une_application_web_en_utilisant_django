from itertools import chain
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import CharField, Value, Q
from django.core.paginator import Paginator

from .models import Ticket, Review, UserFollows
from .forms import SignUpForm, LoginForm, TicketForm, ReviewForm, FollowUserForm


# ===================== AUTHENTIFICATION =====================

def login_view(request):
    """Vue de connexion."""
    if request.user.is_authenticated:
        return redirect('feed')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()
    
    return render(request, 'reviews/login.html', {'form': form})


def signup_view(request):
    """Vue d'inscription."""
    if request.user.is_authenticated:
        return redirect('feed')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Compte créé avec succès !')
            return redirect('feed')
    else:
        form = SignUpForm()
    
    return render(request, 'reviews/signup.html', {'form': form})


@login_required
def logout_view(request):
    """Vue de déconnexion."""
    logout(request)
    return redirect('login')


# ===================== FLUX =====================

@login_required
def feed(request):
    """
    Vue du flux principal.
    Affiche les tickets et critiques des utilisateurs suivis,
    ainsi que les propres posts de l'utilisateur.
    """
    # Récupérer les utilisateurs suivis
    followed_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    
    # Récupérer les tickets visibles (de l'utilisateur + suivis)
    tickets = Ticket.objects.filter(
        Q(user=request.user) | Q(user__in=followed_users)
    ).annotate(content_type=Value('TICKET', CharField()))
    
    # Récupérer les critiques visibles (de l'utilisateur + suivis + réponses aux tickets de l'utilisateur)
    reviews = Review.objects.filter(
        Q(user=request.user) | 
        Q(user__in=followed_users) |
        Q(ticket__user=request.user)
    ).annotate(content_type=Value('REVIEW', CharField()))
    
    # Combiner et trier par date (antéchronologique)
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    
    # Pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Vérifier quels tickets ont déjà une critique de l'utilisateur
    user_reviewed_tickets = Review.objects.filter(user=request.user).values_list('ticket_id', flat=True)
    
    context = {
        'page_obj': page_obj,
        'user_reviewed_tickets': list(user_reviewed_tickets),
    }
    
    return render(request, 'reviews/feed.html', context)


# ===================== TICKETS =====================

@login_required
def create_ticket(request):
    """Vue pour créer un nouveau ticket."""
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, 'Billet créé avec succès !')
            return redirect('feed')
    else:
        form = TicketForm()
    
    return render(request, 'reviews/create_ticket.html', {'form': form})


@login_required
def edit_ticket(request, ticket_id):
    """Vue pour modifier un ticket."""
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, 'Billet modifié avec succès !')
            return redirect('posts')
    else:
        form = TicketForm(instance=ticket)
    
    return render(request, 'reviews/edit_ticket.html', {'form': form, 'ticket': ticket})


@login_required
def delete_ticket(request, ticket_id):
    """Vue pour supprimer un ticket."""
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, 'Billet supprimé avec succès !')
        return redirect('posts')
    
    return render(request, 'reviews/delete_ticket.html', {'ticket': ticket})


# ===================== CRITIQUES =====================

@login_required
def create_review(request, ticket_id):
    """Vue pour créer une critique en réponse à un ticket."""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Vérifier si l'utilisateur a déjà posté une critique pour ce ticket
    if Review.objects.filter(ticket=ticket, user=request.user).exists():
        messages.error(request, 'Vous avez déjà posté une critique pour ce billet.')
        return redirect('feed')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, 'Critique publiée avec succès !')
            return redirect('feed')
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/create_review.html', {
        'form': form,
        'ticket': ticket
    })


@login_required
def create_review_standalone(request):
    """Vue pour créer un ticket et une critique en même temps."""
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            
            messages.success(request, 'Critique publiée avec succès !')
            return redirect('feed')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()
    
    return render(request, 'reviews/create_review_standalone.html', {
        'ticket_form': ticket_form,
        'review_form': review_form
    })


@login_required
def edit_review(request, review_id):
    """Vue pour modifier une critique."""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Critique modifiée avec succès !')
            return redirect('posts')
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'reviews/edit_review.html', {
        'form': form,
        'review': review
    })


@login_required
def delete_review(request, review_id):
    """Vue pour supprimer une critique."""
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Critique supprimée avec succès !')
        return redirect('posts')
    
    return render(request, 'reviews/delete_review.html', {'review': review})


# ===================== POSTS DE L'UTILISATEUR =====================

@login_required
def posts(request):
    """Vue affichant tous les posts de l'utilisateur connecté."""
    tickets = Ticket.objects.filter(user=request.user).annotate(
        content_type=Value('TICKET', CharField())
    )
    reviews = Review.objects.filter(user=request.user).annotate(
        content_type=Value('REVIEW', CharField())
    )
    
    posts_list = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'reviews/posts.html', {'page_obj': page_obj})


# ===================== ABONNEMENTS =====================

@login_required
def subscriptions(request):
    """Vue de gestion des abonnements."""
    if request.method == 'POST':
        form = FollowUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            
            # Vérifier que l'utilisateur ne se suit pas lui-même
            if username == request.user.username:
                messages.error(request, 'Vous ne pouvez pas vous suivre vous-même.')
            else:
                try:
                    user_to_follow = User.objects.get(username=username)
                    
                    # Vérifier si déjà suivi
                    if UserFollows.objects.filter(user=request.user, followed_user=user_to_follow).exists():
                        messages.warning(request, f'Vous suivez déjà {username}.')
                    else:
                        UserFollows.objects.create(
                            user=request.user,
                            followed_user=user_to_follow
                        )
                        messages.success(request, f'Vous suivez maintenant {username}.')
                except User.DoesNotExist:
                    messages.error(request, f"L'utilisateur {username} n'existe pas.")
    else:
        form = FollowUserForm()
    
    # Récupérer les abonnements et abonnés
    following = UserFollows.objects.filter(user=request.user).select_related('followed_user')
    followers = UserFollows.objects.filter(followed_user=request.user).select_related('user')
    
    context = {
        'form': form,
        'following': following,
        'followers': followers,
    }
    
    return render(request, 'reviews/subscriptions.html', context)


@login_required
def unfollow(request, user_id):
    """Vue pour se désabonner d'un utilisateur."""
    user_to_unfollow = get_object_or_404(User, id=user_id)
    follow = get_object_or_404(UserFollows, user=request.user, followed_user=user_to_unfollow)
    
    if request.method == 'POST':
        follow.delete()
        messages.success(request, f'Vous ne suivez plus {user_to_unfollow.username}.')
        return redirect('subscriptions')
    
    return render(request, 'reviews/unfollow.html', {'user_to_unfollow': user_to_unfollow})
