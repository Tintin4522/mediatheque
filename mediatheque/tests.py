from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Emprunteur, Dvd, Cd, Livre, JeuDePlateau
from django.contrib.messages import get_messages


class EmprunteurTests(TestCase):

    def setUp(self):
        self.client = Client()
        # Création d'un utilisateur test
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Connexion de l'utilisateur
        self.client.login(username='testuser', password='testpass')

    def test_create_emprunteur(self):
        response = self.client.post(reverse('create_emprunteur'), {
            'name': 'John Doe',
            'email': 'john@example.com'
        })

        self.assertEqual(response.status_code, 302)

        emprunteur = Emprunteur.objects.filter(name='John Doe').first()
        self.assertIsNotNone(emprunteur)
        self.assertEqual(emprunteur.email, 'john@example.com')
        self.assertEqual(emprunteur.nombre_emprunts, 0)


class AjouterMediaTests(TestCase):
    def setUp(self):
        # Création d'un utilisateur pour les tests
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('ajouter_media')

    def test_ajouter_dvd_valide(self):
        response = self.client.post(self.url, {
            'type_media': 'DVD',
            'submit_type': 'submit',
            'nom_media': 'Test DVD',
            'nb_dispo': '5',
            'nom_realisateur': 'Test Director',
        })

        # Vérifie la redirection après l'ajout
        self.assertEqual(response.status_code, 302)

        # Vérifie que le DVD a été ajouté à la base de données
        self.assertEqual(Dvd.objects.count(), 1)
        dvd = Dvd.objects.first()
        self.assertEqual(dvd.name, 'Test DVD')
        self.assertEqual(dvd.disponible, 5)
        self.assertEqual(dvd.realisateur, 'Test Director')

        # Vérifie le message de succès
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Le média 'Test DVD' a été ajouté avec succès dans la catégorie DVD.")

    def test_ajouter_cd_valide(self):
        response = self.client.post(self.url, {
            'type_media': 'CD',
            'submit_type': 'submit',
            'nom_media': 'Test CD',
            'nb_dispo': '10',
            'nom_artiste': 'Test Artist',
        })

        # Vérifie la redirection après l'ajout
        self.assertEqual(response.status_code, 302)

        # Vérifie que le CD a été ajouté à la base de données
        self.assertEqual(Cd.objects.count(), 1)
        cd = Cd.objects.first()
        self.assertEqual(cd.name, 'Test CD')
        self.assertEqual(cd.disponible, 10)
        self.assertEqual(cd.artiste, 'Test Artist')

        # Vérifie le message de succès
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Le média 'Test CD' a été ajouté avec succès dans la catégorie CD.")

    def test_ajouter_livre_valide(self):
        response = self.client.post(self.url, {
            'type_media': 'Livre',
            'submit_type': 'submit',
            'nom_media': 'Test Book',
            'nb_dispo': '3',
            'nom_auteur': 'Test Author',
        })

        # Vérifie la redirection après l'ajout
        self.assertEqual(response.status_code, 302)

        # Vérifie que le livre a été ajouté à la base de données
        self.assertEqual(Livre.objects.count(), 1)
        livre = Livre.objects.first()
        self.assertEqual(livre.name, 'Test Book')
        self.assertEqual(livre.disponible, 3)
        self.assertEqual(livre.auteur, 'Test Author')

        # Vérifie le message de succès
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Le média 'Test Book' a été ajouté avec succès dans la catégorie Livre.")

    def test_ajouter_media_avec_quantite_inferieure_a_zero(self):
        response = self.client.post(self.url, {
            'type_media': 'Livre',
            'submit_type': 'submit',
            'nom_media': 'Test Book Negative',
            'nb_dispo': '-1',
            'nom_auteur': 'Test Author Negative',
        })

        # Vérifie la redirection après une erreur
        self.assertEqual(response.status_code, 302)

        # Vérifie le message d'erreur
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "La quantité disponible doit être supérieure à 0.")


class UpdateEmprunteurTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        self.emprunteur = Emprunteur.objects.create(name='Old Name')
        self.url = reverse('update_emprunteur', kwargs={'emprunteur_id': self.emprunteur.id})

    def test_update_emprunteur(self):
        response = self.client.post(self.url, {'name': 'New Name'})

        # Vérifie la redirection après la mise à jour
        self.assertEqual(response.status_code, 302)

        # Vérifie que l'emprunteur a été mis à jour dans la base de données
        self.emprunteur.refresh_from_db()
        self.assertEqual(self.emprunteur.name, 'New Name')

        # Vérifie le message de succès
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Le membre a été mis à jour avec succès.")

