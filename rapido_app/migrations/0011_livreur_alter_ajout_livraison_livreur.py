# Generated by Django 4.2.6 on 2025-02-04 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rapido_app', '0010_alter_ajout_livraison_livreur_delete_livreur'),
    ]

    operations = [
        migrations.CreateModel(
            name='Livreur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_prenom', models.CharField(max_length=80)),
                ('sexe', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('disponibilite', models.CharField(default='Oui', max_length=20)),
                ('contact', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='ajout_livraison',
            name='livreur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapido_app.livreur'),
        ),
    ]
