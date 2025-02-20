# Generated by Django 4.2.6 on 2025-02-03 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rapido_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantite', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='produits/')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_prenom', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('contact', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.PositiveIntegerField()),
                ('heure_livraison', models.CharField(max_length=50)),
                ('adresse_livraison', models.TextField()),
                ('date_commande', models.DateTimeField(auto_now_add=True)),
                ('statut', models.CharField(default='En attente', max_length=50)),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapido_app.produit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapido_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='Ajout_Livraison',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.CharField(default='En attente', max_length=50)),
                ('date_livraison', models.DateTimeField(auto_now_add=True)),
                ('commande', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='rapido_app.commande')),
            ],
        ),
    ]
