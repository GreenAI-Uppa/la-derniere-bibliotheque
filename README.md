# La Dernière Bibliothèque


[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)  [![forthebadge](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com)


Bienvenue dans le projet la-dernière-bibliothèque, application web dynamique permettant de maintenir une base de connaissances sur les problèmes du réchauffement climatique, de la destruction de la biodiversité, de la société de (sur)consommation, etc.

Ce repo contient l'architecture python-django MVT (models, views, templates) nécessaire pour lancer l'interface, et ainsi ajouter des fonctionalités au site.

Ce README.md contient les commandes pour lancer une version locale du site https://la-derniere-bibliotheque.org/ sur votre localhost.

## Pour commencer

Pour commencer, vous devez récupérer les données et les modèles, trop volumineux pour le repo. 

Une fois récupéré la base de données (db.sqlite3), les modèles de NLP (models/) et le settings.py, placez-les aux endroits suivants:

la-derniere-bibliotheque/db.sqlite3
la-derniere-bibliotheque/models/
la-derniere-bibliotheque/bddEnv/settings.py
Entrez ici les instructions pour bien débuter avec votre projet...

### Lancement du serveur

Dans un terminal, se placer à l'endroit du fichier manage.py et taper la commande suivante 

> python manage.py runserver

### Navigation sur le site 
Se rendre à l'url suivante : `http://127.0.0.1:8000/`

### Dépendances

Liste des packages à installer :
`pip install django-simple-history`

`pip install numpy`

`pip install -U scikit-learn`

`pip install nltk`

`pip install -U spacy`

`pip install fasttext`

`pip install umap-learn`

## Contributing

Si vous souhaitez contribuer, contactez nous contact@la-derniere-bibliotheque.org pour obtenir les données et les modèles.

## Versions
Listez les versions ici 
_exemple :_
**Dernière version stable :** 5.0
**Dernière version :** 5.1
Liste des versions : [Cliquer pour afficher](https://github.com/your/project-name/tags)
_(pour le lien mettez simplement l'URL de votre projets suivi de ``/tags``)_

## Auteurs
* **GreenAI UPPA** _alias_ [@GreenAI-UPPA](https://github.com/GreenAI-Uppa/)


## License

Ce projet est sous [Licence Creative Commons Attribution - Pas d'Utilisation Commerciale - Pas de Modification 4.0 International](http://creativecommons.org/licenses/by-nc-nd/4.0/).

