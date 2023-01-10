# La Dernière Bibliothèque


[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)  [![forthebadge](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com)


Bienvenue dans le projet la-dernière-bibliothèque, application web dynamique permettant de maintenir une base de connaissances sur les problèmes du réchauffement climatique, de la destruction de la biodiversité, de la société de (sur)consommation, etc.

Ce repo contient l'architecture python-django MVT (models, views, templates) nécessaire pour lancer l'interface, et ainsi ajouter des fonctionalités au site.

Ce README.md contient les commandes pour lancer une version locale du site https://la-derniere-bibliotheque.org/ sur votre localhost.

## Pour commencer

Pour commencer, vous devez récupérer les données et les modèles, trop volumineux pour le repo. 

Une fois récupéré la base de données (db.sqlite3), les modèles de NLP (models/) et le settings.py, placez-les aux endroits suivants:

- la-derniere-bibliotheque/db.sqlite3

- la-derniere-bibliotheque/models/

- la-derniere-bibliotheque/bddEnv/settings.py

Entrez ici les instructions pour bien débuter avec votre projet...

### Lancement du serveur

Dans un terminal, se placer à l'endroit du fichier manage.py et taper la commande suivante 

> python manage.py runserver

Pour un lancement depuis le serveur distant (ovh) avec accès depuis l'extérieur
> python3 manage.py runserver 0.0.0.0:8000

Pour augmenter la verbosité des logs, fixer `DEBUG=True` dans settings.py

### Navigation sur le site 
Se rendre à l'url suivante : `http://127.0.0.1:8000/`

### Modification de la base de données

> python manage.py shell

Then you can play with python in the db, see for instance:
```
from partage.models import Author, Source, Content
Author.objects.all()
Source.objects.all()

print(len(Content.objects.all()),'in the database')

# checking all the contents for a given source
src = "Climat, crises : Le plan de transformation de l'économie française"
for c in Content.objects.all():
  if c.source.titre == src:
      print()
      print(c.text)
```

Note that if you want to modify the objects, django provide specific functions

> element.save() # register in the db the new state of element object

> element.delete() # delete this element from the db. 

In the second case, this will delete every children of elements. So if you delete one source you delete all the contents from this source.

Django provides functions to check dependencies between objects: 
```
from django.contrib.admin.utils import NestedObjects
nested_object = NestedObjects("default")
nested_object.collect([element])
# If you want to delete multi item, you can use:
# nested_object.collect(Model.objects.filter(type="deleted"))

print(nested_object.nested())
```

### Dépendances

Installation des packages :

> pip install -r requirements.txt

Lancer python puis installer la ressource punkt de nltk :

`>>> import nltk`

`>>> nltk.download('punkt')`

## Contributing

Si vous souhaitez contribuer, contactez nous contact@la-derniere-bibliotheque.org pour obtenir les données et les modèles.

## Auteurs
* **GreenAI UPPA** _alias_ [@GreenAI-UPPA](https://github.com/GreenAI-Uppa/)
* Thomas Poupon étudiant CYTECH

## License

Ce projet est sous [Licence Creative Commons Attribution - Pas d'Utilisation Commerciale - Pas de Modification 4.0 International](http://creativecommons.org/licenses/by-nc-nd/4.0/).

