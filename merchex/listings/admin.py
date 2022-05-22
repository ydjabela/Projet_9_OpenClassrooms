from django.contrib import admin
from listings.models import Band, Listing


class BandAdmin(admin.ModelAdmin):  # nous insérons ces deux lignes..
    # liste les champs que nous voulons sur l'affichage de la liste
    list_display = ('name', 'year_formed', 'genre', 'year')


admin.site.register(Band, BandAdmin) # nous modifions cette ligne, en ajoutant un deuxième argument


class ListingAdmin(admin.ModelAdmin):
    # liste les champs que nous voulons sur l'affichage de la liste
    list_display = ('title', 'band')


admin.site.register(Listing, ListingAdmin)
