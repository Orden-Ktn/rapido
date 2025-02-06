from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from .models import *
import time
from plyer import notification
from django.db.models import Count, F, Value, Window
from django.db.models.functions import Rank
from django.contrib.auth.hashers import make_password

#views pour les inscriptions et connexions

def connexion_admin(request):
    return render(request, 'gestionnaire/auth-normal-sign-in.html')

def login_admin(request):
    if request.method == 'POST':
        nom_prenom = request.POST['nom_prenom']
        password = request.POST['password']

        identifiant = Admin.objects.filter(nom_prenom=nom_prenom, password=password).first()
        clients = User.objects.all()
        total_produits = Produit.objects.count()
        total_clients = User.objects.count()
        total_livraisons = Ajout_Livraison.objects.filter(statut='Effectuée').count()  
        total_livreurs = Livreur.objects.count()
       
        request.session['user_nom'] = identifiant.nom_prenom
        if identifiant:
            
            return render(request, 'gestionnaire/index.html', {
            'total_produits': total_produits,
            'clients': clients,
            'user_nom': identifiant.nom_prenom,
            'total_clients': total_clients,
            'total_livraisons': total_livraisons,
            'total_livreurs': total_livreurs
    })

        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
            return render(request, 'gestionnaire/auth-normal-sign-in.html')
        
    return render(request, 'gestionnaire/auth-normal-sign-in.html')

def validate_inscription_livreur(request):
    if request.method == "POST":
        nom_prenom = request.POST.get("nom_prenom")
        contact = request.POST.get("contact")
        email = request.POST.get("email")
        sexe = request.POST.get("sexe")
        password = request.POST.get("password")

        if Livreur.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect("inscription_livreur")
        
        if Livreur.objects.filter(nom_prenom=nom_prenom).exists():
            messages.error(request, "Ce nom et prénom sont déjà utilisés.")
            return redirect("inscription_livreur")

        if Livreur.objects.filter(contact=contact).exists():
            messages.error(request, "Ce contact est déjà utilisé.")
            return redirect("inscription_livreur")

        Livreur.objects.create(
            nom_prenom=nom_prenom,
            sexe=sexe,
            contact=contact,
            email=email,
            password=make_password(password), 
        )

        messages.success(request, "Inscription réussie ! Vous pouvez maintenant vous connecter.")
        return redirect("connexion_livreur") 

    return render(request, "livreur/auth-sign-up.html")

def inscription_livreur(request):
    return render(request, 'livreur/auth-sign-up.html')

def login_livreur(request):
    return render(request, 'livreur/auth-normal-sign-in.html')

def validate_connexion_livreur(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        identifiant = Livreur.objects.filter(email=email).first()

        total_produits = Produit.objects.count()
        total_livraisons = Ajout_Livraison.objects.count()

        if identifiant and check_password(password, identifiant.password):
            request.session['user_id'] = identifiant.id
            request.session['user_nom'] = identifiant.nom_prenom
            request.session['user_disponibilite'] = identifiant.disponibilite
            return redirect('index_livreur')
        else:
            messages.error(request, 'Email ou mot de passe incorrect.')
            return render(request, 'livreur/auth-normal-sign-in.html')
        
    return render(request, 'livreur/index.html', {
            'total_produits': total_produits,
            'total_livraisons': total_livraisons
    })

def deconnexion_admin(request):
    request.session.flush()
    return redirect('login_admin')

def deconnexion_livreur(request):
    request.session.flush()
    return redirect('connexion_livreur')

def deconnexion_user(request):
    request.session.flush()
    return redirect('connexion_user')

def connexion_livreur(request):
    return render(request, 'livreur/auth-normal-sign-in.html')

def connexion_user(request):
    return render(request, 'users/connexion.html')

def inscription_user(request):
    return render(request, 'users/register.html')

def validate_inscription_user(request):
    if request.method == "POST":
        nom_prenom = request.POST.get("nom_prenom")
        contact = request.POST.get("contact")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return redirect("inscription_user")

        if User.objects.filter(contact=contact).exists():
            messages.error(request, "Ce contact est déjà utilisé.")
            return redirect("inscription_user")

        User.objects.create(
            nom_prenom=nom_prenom,
            contact=contact,
            email=email,
            password=make_password(password),  
        )

        messages.success(request, "Inscription réussie ! Vous pouvez maintenant vous connecter.")
        return redirect(request.META.get('HTTP_REFERER', '/')) 

    return render(request, "users/register.html")

def validate_connexion_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.filter(email=email).first()

        if user and check_password(password, user.password): 
            request.session['user_id'] = user.id
            request.session['user_nom'] = user.nom_prenom

            produits = Produit.objects.all()
            commandes = Commande.objects.filter(user=user)

            if user:
                return render(request, 'users/index.html', {
                    "produits": produits,
                    "commandes": commandes,
                    "user_nom": user.nom_prenom
                })         

        else:
            messages.error(request, 'Email ou mot de passe incorrect.')
            return redirect(request.META.get('HTTP_REFERER', '/')) 

    return render(request, 'users/connexion.html') 



#Views pour le gestionnaire

def index_gestionnaire(request):
    clients = User.objects.all()
    total_produits = Produit.objects.count()
    total_clients = User.objects.count()
    total_livraisons = Ajout_Livraison.objects.filter(statut="Effectuée").count() 
    total_livreurs = Livreur.objects.count()
    
    return render(request, 'gestionnaire/index.html', {'clients': clients, 'total_produits': total_produits,
            'total_clients': total_clients,
            'total_livraisons': total_livraisons,
            'total_livreurs': total_livreurs})

def ajout_produit(request):
    return render(request, 'gestionnaire/add_produit.html')

def all_produit(request):
    produits = Produit.objects.all()
    return render(request, 'gestionnaire/all_produit.html', {'produits': produits})

def add_produit(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        prix = request.POST.get('prix')
        quantite = request.POST.get('quantite')
        image = request.FILES.get('image')  

        if not (nom and prix and quantite):  
            return render(request, 'gestionnaire/add_produit.html', {
                'error': "Tous les champs sont obligatoires."
            })

        Produit.objects.create(nom=nom, prix=prix, quantite=quantite, image=image)
        messages.success(request, 'Produit ajouté')
        return redirect('ajout_produit')

    return render(request, 'gestionnaire/all_produit.html')

def add_livraison(request):
    commandes = Commande.objects.filter(statut='En attente') 
    livreurs = Livreur.objects.filter(disponibilite='Oui')
    return render(request, 'gestionnaire/add_course.html', {"commandes": commandes, "livreurs": livreurs})

def enregistrer_affectation(request):
    if request.method == 'POST':
        commande_id = request.POST.get('commande_id')
        livreur_id = request.POST.get(f'livreur_{commande_id}')

        print(f"Commande ID reçu: {commande_id}, Livreur ID reçu: {livreur_id}") 

        if commande_id and livreur_id:
            try:
                commande = Commande.objects.get(id=commande_id)
                produit = commande.produit  
                livreur = Livreur.objects.get(id=livreur_id) 
                affectation = Ajout_Livraison(
                    commande=commande,
                    produit=produit,
                    livreur=livreur,
                    statut="En cours"
                )
                affectation.save()
                commande.statut = "En cours"
                commande.save()

                messages.success(request, 'Livraison attribuée !') 
                return redirect(request.META.get('HTTP_REFERER', '/'))

            except Commande.DoesNotExist:
                print("❌ Erreur: Commande introuvable")
            except User.DoesNotExist:
                print("❌ Erreur: Livreur introuvable")

    return redirect('add_livraison')  


def update_livraison(request):
    if request.method == "POST":
        commande_id = request.POST.get('commande_id')
        
        if commande_id:
            try:
                livraison = get_object_or_404(Ajout_Livraison, id=commande_id)

                livraison.statut = 'Effectuée'
                livraison.save()

                commande = livraison.commande
                commande.statut = 'Effectuée'
                commande.save()

                messages.success(request, 'Livraison effectuée avec succès !')
                return redirect(request.META.get('HTTP_REFERER', '/'))
            
            except Ajout_Livraison.DoesNotExist:
                return HttpResponse("Commande non trouvée.", status=404)

    return redirect('livreur:recapitulatif') 

def delete_livreur(request, id):
    objet = Livreur.objects.get(pk=id)
    objet.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def delete_produit(request, id):
    objet = Produit.objects.get(pk=id)
    objet.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def update_prix(request, produit_id):
    if request.method == 'POST':
        nouveau_prix = request.POST.get('prix')

        if nouveau_prix:
            produit = get_object_or_404(Produit, id=produit_id)
            produit.prix = nouveau_prix
            produit.save()
            messages.success(request, f"Le prix de {produit.nom} a été mis à jour !")
        else:
            messages.error(request, "Veuillez entrer un prix valide.")

    return redirect(request.META.get('HTTP_REFERER', '/'))

def update_quantite(request, produit_id):
    if request.method == 'POST':
        nouvelle_quantite = int(request.POST.get('quantite'))

        if nouvelle_quantite:
            produit = get_object_or_404(Produit, id=produit_id)
            produit.quantite = int(produit.quantite) + nouvelle_quantite
            produit.save()
            messages.success(request, f"Le quantité de {produit.nom} a été mis à jour !")
        else:
            messages.error(request, "Veuillez entrer un quantité valide.")

    return redirect(request.META.get('HTTP_REFERER', '/'))



#Views pour les livreurs

def index_livreur(request):
    livreur_id = request.session.get('user_id')
    commandes = Ajout_Livraison.objects.filter(livreur_id=livreur_id, statut='En cours')
    total_produits = Produit.objects.count()
    total_livraisons = Ajout_Livraison.objects.filter(statut="Effectuée").count()
    
    return render(request, 'livreur/index.html', {
        'commandes': commandes,
        'total_produits': total_produits,
        'total_livraisons': total_livraisons,
        'user_nom': request.session.get('user_nom')  
    })


def all_livreur(request):
    livreurs = Livreur.objects.all()
    return render(request, 'gestionnaire/all_livreur.html', {'livreurs': livreurs})

def recapitulatif(request):
    total_livraisons = Ajout_Livraison.objects.filter(statut="Effectuée").count()
    total_produits = Produit.objects.count()
    return render(request, 'livreur/recapitulatif.html',
    {
        'total_produits': total_produits,
        'total_livraisons': total_livraisons,
    })


def historique_livraison(request):
    courses = Ajout_Livraison.objects.filter(statut='En cours')
    livraisons = Ajout_Livraison.objects.filter(statut='Effectuée')
    return render(request, 'gestionnaire/historique.html', {'courses': courses, 'livraisons': livraisons})

def dispo(request):
    if request.method == "POST":
        id_livreur = request.POST.get('id_livreur')

        if id_livreur:
            statut = get_object_or_404(Livreur, id=id_livreur)

            statut.disponibilite = 'Oui'
            statut.save()

            messages.success(request, 'Votre disponibilité est mise à jour!')
            return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect('index_livreur')

def non_dispo(request):
    if request.method == "POST":
        id_livreur = request.POST.get('id_livreur')

        if id_livreur:
            statut = get_object_or_404(Livreur, id=id_livreur)

            statut.disponibilite = 'Non'
            statut.save()

            messages.success(request, 'Votre disponibilité est mise à jour!')
            return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect('index_livreur')


#Views pour les clients

def add_commande(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        produit_id = request.POST.get('produit_id')
        quantite = int(request.POST.get('quantite'))
        heure = request.POST.get('heure')
        adresse = request.POST.get('adresse')

        try:
            produit = Produit.objects.get(id=produit_id)
        except Produit.DoesNotExist:
            messages.error(request, "Le produit sélectionné n'existe pas.")
            return redirect('add_commande')

        try:
            quantite = int(quantite)
        except ValueError:
            messages.error(request, "Veuillez entrer une quantité valide.")
            return redirect('add_commande')

        if quantite > int(produit.quantite):
            messages.error(request, "Stock insuffisant pour ce produit.")
            return redirect('add_commande')

        commande = Commande.objects.create(
            user_id=user_id,
            produit_id=produit_id,
            quantite=quantite,
            heure_livraison=heure,
            adresse_livraison=adresse,
            statut="En attente"
        )

        produit.quantite = int(produit.quantite) - quantite
        produit.save()

        messages.success(request, "Commande ajoutée avec succès.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'users/dashboard/add_commande.html')

def user_dashboard(request):
    produits = Produit.objects.all()
    return render(request, 'users/index.html', {'produits': produits})

def form_commande(request):
    return render(request, 'users/add_commande.html')

def mon_panier(request):
     if request.method == "POST":
        user_id = request.POST.get('user_id')
        commandes = Commande.objects.filter(user_id=user_id)
        
        return render(request, 'users/mon_panier.html', {
            'commandes': commandes,
            'user_nom': request.session.get('user_nom')  
        })