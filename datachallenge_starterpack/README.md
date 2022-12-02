# Data Challenge La Dernière Bibliothèque


Bienvenue dans le data challenge du projet la-dernière-bibliothèque. Votre mission, si vous l'acceptez, sera d'améliorer l'application web dynamique pour faire grandir une base de données de connaissances et une interface ludique sur les problèmes environnementaux.

Ce dossier contient tous les éléments pour vous lancer dans la compétition et construire vos modèles de NLP. Il vient compléter le repo dédié à l'architecture python-django.

## Description des fichiers

### le fichier contents.json
Ce fichier est un extraction des données de la base sqlite. Il contient la liste des 981 contenus disponibles à ce jour sur le projet, avec, pour chaque contenu, la liste de tags associés. 

### le fichier GreenAI_DATA_CHALLENGE.pdf
La présentation pdf de présentation du sujet, que vous avez entendu vendredi soir, avec des liens utiles, comme le Tutoriel Django, pour se lancer avec ce framework python.

## Lien vers les données Twitter et le modèle actuel en production
Ce challenge consiste à améliorer le modèle de NLP fasttext en production sur le site actuel. Ce modèle a été entraîné cet été à l'aide des premiers contenus (300 environs à l'époque) et un ensemble de tweets issus de la communauté Bonpote, sur la période de l'élection présidentielle de cette année.

Le lien filetransfer [https://filesender.renater.fr/?s=download&token=fe1b1505-59da-4ab9-9194-156e282349a3](https://filesender.renater.fr/?s=download&token=fe1b1505-59da-4ab9-9194-156e282349a3) contient :

- l'intégralité des données Twitter, représentant plus de 80k comptes et plus de 1,6M de tweets (600 Mo environ),
- un script python permettant de se lancer dans l'extraction des tweets,
- le modèle fasttext déjà en production.

## Auteurs
* **GreenAI UPPA** _alias_ [@GreenAI-UPPA](https://github.com/GreenAI-Uppa/)


## License
Ce projet est sous [Licence Creative Commons Attribution - Pas d'Utilisation Commerciale - Pas de Modification 4.0 International](http://creativecommons.org/licenses/by-nc-nd/4.0/).

