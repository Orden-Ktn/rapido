from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class User(models.Model):
    nom_prenom = models.CharField(max_length=100)
    contact = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Vérifie si le mot de passe n'est pas déjà haché
        if not self.password.startswith("pbkdf2_sha256$"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom_prenom

class Admin(models.Model):
    nom_prenom = models.CharField(max_length=80)
    password = models.CharField(max_length=100)


class Produit(models.Model):
    nom = models.CharField(max_length=255)
    prix = models.CharField(max_length=150)
    quantite = models.CharField(max_length=150)
    image = models.ImageField(upload_to='produits/', null=True, blank=True)  # Dossier de stockage

class Commande(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Ajout de l'utilisateur
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    heure_livraison = models.CharField(max_length=50)
    adresse_livraison = models.TextField()
    date_commande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=50, default="En attente")

    def __str__(self):
        return f"Commande de {self.user.nom_prenom} - {self.produit.nom} - {self.quantite} unités"


class Livreur(models.Model):
    nom_prenom = models.CharField(max_length=80)
    sexe = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    disponibilite = models.CharField(max_length=20, default='Oui')
    contact = models.CharField(max_length=30)
    password = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        # Vérifie si le mot de passe n'est pas déjà haché
        if not self.password.startswith("pbkdf2_sha256$"):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom_prenom} ({'Disponible' if self.disponibilite else 'Indisponible'})"
    

class Ajout_Livraison(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    livreur = models.ForeignKey(Livreur, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    statut = models.CharField(max_length=50, default="En cours")

    def __str__(self):
        return f"Livraison {self.id} - {self.produit.nom} par {self.livreur.nom_prenom}"