from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Cd, Media, Dvd, Livre, Emprunteur, Emprunt, JeuDePlateau
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index(request):
    return render(request, 'index.html')


def personnel(request):
    return render(request, 'personnel.html')


@login_required
def gestion(request):
    return render(request, 'gestion.html')


@login_required
def liste_membres(request):
    emprunteurs = Emprunteur.objects.all()
    return render(request, 'list_membres.html', {'emprunteurs': emprunteurs})


def consultation(request):
    query = request.GET.get('name', '')

    cd_results = Cd.objects.filter(name__icontains=query)
    dvd_results = Dvd.objects.filter(name__icontains=query)
    livre_results = Livre.objects.filter(name__icontains=query)
    jeux_results = JeuDePlateau.objects.filter(name__icontains=query)

    return render(request, 'consultation.html',
                  {'cds': cd_results,
                   'dvds': dvd_results,
                   'livres': livre_results,
                   'jeux': jeux_results})


@login_required
def list_media(request):
    query = request.GET.get('name', '')

    cd_results = Cd.objects.filter(name__icontains=query)
    dvd_results = Dvd.objects.filter(name__icontains=query)
    livre_results = Livre.objects.filter(name__icontains=query)
    jeux_results = JeuDePlateau.objects.filter(name__icontains=query)

    return render(request, 'list_media.html',
                  {'cds': cd_results,
                   'dvds': dvd_results,
                   'livres': livre_results,
                   'jeux': jeux_results})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.POST.get('next', 'gestion')
            return redirect(next_url)
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'personnel.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login_view')


@login_required
def create_emprunteur(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']

        Emprunteur.objects.create(name=name, email=email)
        messages.success(request, "Emprunteur ajouté avec succès.")
        return redirect('create_emprunteur')

    return render(request, 'create_emprunteur.html')


@login_required
def list_emprunteurs(request):
    emprunteurs = Emprunteur.objects.all()
    return render(request, 'list_membres.html', {'emprunteurs': emprunteurs})


@login_required
def ajouter_emprunt(request):
    emprunteurs = Emprunteur.objects.all()
    selected_emprunteur_id = None
    selected_type = None
    medias = []

    if request.method == 'POST':
        emprunteur_id = request.POST.get('emprunteur')
        type_media = request.POST.get('type_media')
        selected_emprunteur_id = emprunteur_id
        selected_type = type_media

        if type_media:
            if type_media == 'DVD':
                medias = Dvd.objects.all()
            elif type_media == 'CD':
                medias = Cd.objects.all()
            elif type_media == 'Livre':
                medias = Livre.objects.all()

        if 'media' in request.POST:
            media_id = request.POST.get('media')
            try:
                emprunteur = Emprunteur.objects.get(id=emprunteur_id)

                if emprunteur.nombre_emprunts >= 3:
                    messages.error(request, f"{emprunteur.name} a déjà atteint la limite de 3 emprunts.")
                    return redirect('ajouter_emprunt')

                if type_media == 'DVD':
                    media = Dvd.objects.get(id=media_id)
                elif type_media == 'CD':
                    media = Cd.objects.get(id=media_id)
                elif type_media == 'Livre':
                    media = Livre.objects.get(id=media_id)

                if media.disponible > 0:
                    Emprunt.objects.create(emprunteur=emprunteur, media=media,
                                           date_retour=timezone.now() + timedelta(weeks=1))

                    media.disponible -= 1
                    media.save()

                    emprunteur.nombre_emprunts += 1
                    emprunteur.save()

                    messages.success(request, f"L'emprunt de {media.name} a été ajouté pour {emprunteur.name}.")
                    return redirect('ajouter_emprunt')
                else:
                    messages.error(request, f"{media.name} n'est pas disponible actuellement.")

            except (Emprunteur.DoesNotExist, Dvd.DoesNotExist, Cd.DoesNotExist, Livre.DoesNotExist):
                messages.error(request, "Erreur lors de l'ajout de l'emprunt.")
                return redirect('ajouter_emprunt')

    return render(request, 'ajout_emprunt.html', {
        'emprunteurs': emprunteurs,
        'selected_emprunteur_id': selected_emprunteur_id,
        'selected_type': selected_type,
        'medias': medias
    })


@login_required
def liste_emprunts(request):
    emprunts = Emprunt.objects.filter()
    return render(request, 'list_emprunts.html', {'emprunts': emprunts})


@login_required
def marquer_comme_rendu(request, emprunt_id):
    if request.method == 'POST':
        emprunt = get_object_or_404(Emprunt, id=emprunt_id)
        emprunt.date_retour = timezone.now()
        emprunt.save()

        media = emprunt.media
        media.disponible += 1
        media.save()

        emprunteur = emprunt.emprunteur

        emprunteur.nombre_emprunts -= 1
        emprunteur.save()

        emprunt.delete()

        messages.success(request, "Emprunt marqué comme rendu.")
        return redirect('liste_emprunts')
    else:
        messages.error(request, "Une erreur est survenue.")
        return redirect('liste_emprunts')


@login_required
def ajouter_media(request):
    selected_type = None

    if request.method == 'POST':
        type_media = request.POST.get('type_media')
        selected_type = type_media

        if 'submit_type' in request.POST:
            nom_media = request.POST.get('nom_media')
            nb_dispo = request.POST.get('nb_dispo')
            nom_realisateur = request.POST.get('nom_realisateur')
            nom_auteur = request.POST.get('nom_auteur')
            nom_artiste = request.POST.get('nom_artiste')
            createur_jeu = request.POST.get('createur_jeu')

            if type_media and nom_media and nb_dispo:
                try:
                    nb_dispo = int(nb_dispo)
                    if nb_dispo <= 0:
                        messages.error(request, "La quantité disponible doit être supérieure à 0.")
                        return redirect('ajouter_media')

                    if type_media == 'DVD':
                        Dvd.objects.create(name=nom_media, realisateur=nom_realisateur, disponible=nb_dispo)
                    elif type_media == 'CD':
                        Cd.objects.create(name=nom_media, artiste=nom_artiste, disponible=nb_dispo)
                    elif type_media == 'Livre':
                        Livre.objects.create(name=nom_media, auteur=nom_auteur, disponible=nb_dispo)
                    elif type_media == 'JeuDePlateau':
                        JeuDePlateau.objects.create(name=nom_media, createur=createur_jeu)

                    messages.success(request, f"Le média '{nom_media}' a été ajouté avec succès dans la catégorie {type_media}.")
                    return redirect('ajouter_media')

                except Exception as e:
                    logger.error(f"Erreur lors de l'ajout du média: {e}")
                    messages.error(request, "Erreur lors de l'ajout du média.")
                    return redirect('ajouter_media')

    return render(request, 'ajout_media.html', {'selected_type': selected_type})


@login_required
def update_emprunteur(request, emprunteur_id):
    emprunteur = get_object_or_404(Emprunteur, id=emprunteur_id)

    if request.method == 'POST':
        new_name = request.POST.get('name')
        if new_name:
            emprunteur.name = new_name
            emprunteur.save()
            messages.success(request, "Le membre a été mis à jour avec succès.")
            return redirect('list_emprunteurs')
        else:
            messages.error(request, "Le nom ne peut pas être vide.")

    return render(request, 'update_emprunteur.html', {'emprunteur': emprunteur})


@login_required
def delete_emprunteur(request, emprunteur_id):
    emprunteur = get_object_or_404(Emprunteur, id=emprunteur_id)

    if request.method == 'POST':
        emprunteur.delete()
        messages.success(request, "Le membre a été supprimé avec succès.")
        return redirect('list_emprunteurs')

    return render(request, 'delete_emprunteur.html', {'emprunteur': emprunteur})
