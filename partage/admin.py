from django.contrib import admin
from .models import Author
from .models import Tag
from .models import Source
from .models import Content
from .models import Resultat_jeu1
from .models import Resultat_jeu2

admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Source)
admin.site.register(Content)
admin.site.register(Resultat_jeu1)
admin.site.register(Resultat_jeu2)

