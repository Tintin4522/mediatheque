from django.db import models
from django.utils import timezone


class Emprunteur(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    nombre_emprunts = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Media(models.Model):
    name = models.CharField(max_length=255)
    date_emprunt = models.DateTimeField(auto_now_add=True)
    disponible = models.IntegerField(default=1)
    emprunteur = models.ForeignKey(Emprunteur, on_delete=models.CASCADE, related_name='emprunts', null=True, blank=True)

    def __str__(self):
        if self.emprunteur:
            return f"Emprunté par {self.emprunteur.name} le {self.date_emprunt.strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            return "Disponible"


class Livre(Media):
    auteur = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} par {self.auteur}"

class Dvd(Media):
    realisateur = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        if self.realisateur:
            return f"{self.name} Réalisé par: {self.realisateur}"
        return f"{self.name}"


class Cd(Media):
    artiste = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} Artiste: {self.artiste}"


class Emprunt(models.Model):
    emprunteur = models.ForeignKey(Emprunteur, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(default=timezone.now)
    date_retour = models.DateTimeField()

    def est_en_retard(self):
        return self.date_retour < timezone.now()

    def __str__(self):
        return f"{self.emprunteur.name} - {self.media.name} ({self.date_emprunt} - {self.date_retour})"


class JeuDePlateau(models.Model):
    name = models.CharField(max_length=255)
    createur = models.CharField(max_length=255)