from django.urls import path
from django.contrib import admin
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('index_gestionnaire', views.index_gestionnaire, name='index_gestionnaire'),
    path('', views.login_admin, name='login_admin'),
    path('gestionnaire', views.connexion_admin, name='connexion_admin'),
    path('deconnexion_admin', views.deconnexion_admin, name='deconnexion_admin'),

    path('livreur', views.login_livreur, name='login_livreur'),
    path('validate_connexion_livreur', views.validate_connexion_livreur, name='validate_connexion_livreur'),    
    path('index_livreur', views.index_livreur, name='index_livreur'),
    path('inscription_livreur', views.inscription_livreur, name='inscription_livreur'),
    path('connexion_livreur', views.connexion_livreur, name='connexion_livreur'),
    path('validate_inscription_livreur', views.validate_inscription_livreur, name='validate_inscription_livreur'),
    path('all_livreur', views.all_livreur, name='all_livreur'),
    path('delete_livreur/<int:id>/', views.delete_livreur, name='delete_livreur'),
    path('dispo', views.dispo, name='dispo'),
    path('non_dispo', views.non_dispo, name='non_dispo'),
    path('deconnexion_livreur', views.deconnexion_livreur, name='deconnexion_livreur'),


    path('validate_inscription_user', views.validate_inscription_user, name='validate_inscription_user'),
    path('deconnexion_user', views.deconnexion_user, name='deconnexion_user'),
    path('connexion_user', views.connexion_user, name='connexion_user'),
    path('inscription_user', views.inscription_user, name='inscription_user'),
    path('user_dashboard', views.user_dashboard, name='user_dashboard'),
    path('mon_panier', views.mon_panier, name='mon_panier'),
    path('validate_connexion_user', views.validate_connexion_user, name='validate_connexion_user'),


    path('add_commande', views.add_commande, name='add_commande'),
    path('form_commande', views.form_commande, name='form_commande'),


    path('add_produit', views.add_produit, name='add_produit'),
    path('all_produit', views.all_produit, name='all_produit'),
    path('ajout_produit', views.ajout_produit, name='ajout_produit'),
    path('delete_produit/<int:id>/', views.delete_produit, name='delete_produit'),
    path('update_prix/<int:produit_id>/', views.update_prix, name='update_prix'),
    path('update_quantite/<int:produit_id>/', views.update_quantite, name='update_quantite'),


    path('add_livraison', views.add_livraison, name='add_livraison'),
    path("enregistrer_affectation", views.enregistrer_affectation, name="enregistrer_affectation"),
    path("update_livraison", views.update_livraison, name="update_livraison"),
    path("historique_livraison", views.historique_livraison, name="historique_livraison"),
    path("recapitulatif", views.recapitulatif, name="recapitulatif"),

    


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
