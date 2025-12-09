# LITReview

Application web Django permettant de demander et publier des critiques de livres et d'articles.

## 📋 Description

LITReview est une plateforme communautaire où les utilisateurs peuvent :
- **Demander des critiques** en créant des billets (tickets) pour des livres ou articles
- **Publier des critiques** en réponse aux billets d'autres utilisateurs
- **Créer des critiques autonomes** (billet + critique en une seule étape)
- **Suivre d'autres utilisateurs** pour voir leurs publications dans leur flux
- **Gérer leurs publications** (modifier, supprimer)

## 🚀 Installation

### Prérequis
- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone <url-du-repository>
cd litreview_project
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**

Sur Linux/macOS :
```bash
source venv/bin/activate
```

Sur Windows :
```bash
venv\Scripts\activate
```

4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

5. **Appliquer les migrations**
```bash
python manage.py migrate
```

6. **Créer les données de test (optionnel)**
```bash
python create_test_data.py
```

7. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

8. **Accéder à l'application**
Ouvrir un navigateur et aller à : http://127.0.0.1:8000/

## 👤 Comptes de test

Si vous avez exécuté le script de données de test, les comptes suivants sont disponibles :

| Utilisateur | Mot de passe | Rôle |
|-------------|--------------|------|
| admin | admin123 | Superutilisateur |
| jean_5679 | testpass123 | Utilisateur |
| sarahj | testpass123 | Utilisateur |
| severine123 | testpass123 | Utilisateur |

## 📁 Structure du projet

```
litreview_project/
├── config/                    # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── reviews/                   # Application principale
│   ├── migrations/
│   ├── templates/
│   │   └── reviews/
│   │       ├── snippets/
│   │       │   ├── ticket_snippet.html
│   │       │   └── review_snippet.html
│   │       ├── login.html
│   │       ├── signup.html
│   │       ├── feed.html
│   │       ├── posts.html
│   │       ├── subscriptions.html
│   │       └── ...
│   ├── admin.py
│   ├── forms.py
│   ├── models.py              # Ticket, Review, UserFollows
│   ├── urls.py
│   └── views.py
├── templates/                 # Templates globaux
│   └── base.html
├── static/                    # Fichiers statiques
├── media/                     # Fichiers uploadés
├── db.sqlite3                 # Base de données SQLite
├── manage.py
├── requirements.txt
├── create_test_data.py        # Script de données de test
└── README.md
```

## 🔧 Fonctionnalités

### Authentification
- Inscription avec nom d'utilisateur et mot de passe
- Connexion / Déconnexion
- Protection des pages (accès réservé aux utilisateurs connectés)

### Gestion des billets (Tickets)
- Créer un billet pour demander une critique
- Modifier ses propres billets
- Supprimer ses propres billets
- Ajouter une image au billet

### Gestion des critiques (Reviews)
- Créer une critique en réponse à un billet existant
- Créer une critique autonome (billet + critique)
- Modifier ses propres critiques
- Supprimer ses propres critiques
- Système de notation de 0 à 5 étoiles

### Flux
- Affichage des billets et critiques des utilisateurs suivis
- Affichage de ses propres publications
- Affichage des réponses à ses propres billets
- Tri antéchronologique
- Pagination

### Abonnements
- Suivre d'autres utilisateurs
- Se désabonner
- Voir la liste de ses abonnements
- Voir la liste de ses abonnés

## 📜 Conformité

Ce projet respecte :
- Les directives de la PEP8
- Le schéma de base de données fourni
- Les wireframes de l'UX designer
- Les bonnes pratiques d'accessibilité WCAG

## 🛠️ Technologies utilisées

- **Backend** : Django 5.x
- **Base de données** : SQLite3
- **Frontend** : HTML5, CSS3, Bootstrap 5
- **Icônes** : Bootstrap Icons
- **Images** : Pillow (gestion des uploads)

## 📝 License

Projet réalisé dans le cadre de la formation OpenClassrooms.
