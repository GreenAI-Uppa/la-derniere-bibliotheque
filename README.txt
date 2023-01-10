Bienvenue dans le projet la-dernière-bibliothèque

Ce README.txt contient les commandes pour lancer une version locale sur votre machine du site https://la-derniere-bibliotheque.org/.

Il contient l'architecture python-django MVT (models, views, templates) nécessaire pour ajouter des fonctionalités à l'interface.

Première étape :
Une fois récupéré la base de données (db.sqlite3), les modèles de NLP (models/) et le settings.py, placez-les aux endroits suivants:
la-derniere-bibliotheque/db.sqlite3
la-derniere-bibliotheque/models/
la-derniere-bibliotheque/bddEnv/settings.py

Deuxième étape :
Dans un terminal, se placer à l'endroit du fichier manage.py et taper la commande suivante 

>>> python manage.py runserver

Troisième étape :
Se rendre à l'url suivante : `http://127.0.0.1:8000/`

Liste des packages à installer :
`pip install django-simple-history`
`pip install numpy`
`pip install -U scikit-learn`
`pip install nltk`
`pip install -U spacy`
`pip install fasttext`
`pip install umap-learn`
`
python3
>>> import nltk
>>> nltk.download('punkt')
`
