from django.contrib import admin
from django.urls import path
from mediatheque.views import index, personnel, consultation, gestion, login_view, create_emprunteur, liste_membres, \
    list_emprunteurs, ajouter_emprunt, marquer_comme_rendu, liste_emprunts, list_media, ajouter_media, logout_view, \
    update_emprunteur, delete_emprunteur

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('personnel/', personnel, name='personnel'),
    path('consultation/', consultation, name='consultation'),
    path('list_media/', list_media, name='list_media'),
    path('gestion/', gestion, name='gestion'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('creation-emprunteur/', create_emprunteur, name='create_emprunteur'),
    path('liste-membres/', liste_membres, name='liste_membres'),
    path('emprunteurs/', list_emprunteurs, name='list_emprunteurs'),
    path('ajouter-emprunt/', ajouter_emprunt, name='ajouter_emprunt'),
    path('ajouter-media/', ajouter_media, name='ajouter_media'),
    path('emprunts/', liste_emprunts, name='liste_emprunts'),
    path('emprunts/<int:emprunt_id>/marquer_comme_rendu/', marquer_comme_rendu, name='marquer_comme_rendu'),
    path('emprunteurs/<int:emprunteur_id>/update/', update_emprunteur, name='update_emprunteur'),
    path('emprunteurs/<int:emprunteur_id>/delete/', delete_emprunteur, name='delete_emprunteur'),
]
