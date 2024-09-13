from django.contrib import admin
from .models import Emprunteur, Livre, Dvd, Cd, Emprunt

admin.site.register(Emprunteur)
admin.site.register(Livre)
admin.site.register(Dvd)
admin.site.register(Cd)
admin.site.register(Emprunt)
