# Data Challenge La Dernière Bibliothèque


Bienvenue dans le data challenge du projet la-dernière-bibliothèque. Votre mission, si vous l'acceptez, sera d'améliorer l'application web dynamique pour faire grandir une base de données de connaissances et une interface ludique sur les problèmes environnementaux.

Ce dossier contient tous les éléments pour vous lancer dans la compétition et construire vos modèles de NLP. Il vient compléter le repo dédié à l'architecture python-django.

## Description des fichiers

### le fichier contents.json
Ce fichier est un extraction des données de la base sqlite. Il contient la liste des 981 contenus disponibles à ce jour sur le projet, avec, pour chaque contenu, la liste de tags associés. 

### le fichier GreenAI_DATA_CHALLENGE.pdf
La présentation pdf de présentation du sujet, que vous avez entendu vendredi soir, avec des liens utiles, comme le Tutoriel Django, pour se lancer avec ce framework python.

### le fichier queries_test.csv
Ce fichier vous permettra d'évaluer votre moteur de recherche. Plus d'explications ci-dessous dans la partie évaluation.

## Lien vers les données Twitter et le modèle actuel en production
Ce challenge consiste à améliorer le modèle de NLP fasttext en production sur le site actuel. Ce modèle a été entraîné cet été à l'aide des premiers contenus (300 environs à l'époque) et un ensemble de tweets issus de la communauté Bonpote, sur la période de l'élection présidentielle de cette année.

Le lien filetransfer [https://filesender.renater.fr/?s=download&token=fe1b1505-59da-4ab9-9194-156e282349a3](https://filesender.renater.fr/?s=download&token=fe1b1505-59da-4ab9-9194-156e282349a3) contient :

- l'intégralité des données Twitter, représentant plus de 80k comptes et plus de 1,6M de tweets (600 Mo environ),
- un script python permettant de se lancer dans l'extraction des tweets,
- le modèle fasttext déjà en production.

## Procédure d'évaluation du Moteur de Recherche
Déterminer le meilleur algorithme de recherche n'est pas une tâche facile. Pour attester des bonnes performances de votre moteur de recherche suite à l'entraînement de nouveaux modèles de NLP, de nombreuses solutions peuvent être imaginées. 
Pour garantir une mesure quantitative, nous mettons à votre disposition :
- un fichier queries_test.csv qui contient 28 requêtes que nous avons sélectionnés avec les 28 contenus identifiés comme idéal et que doit ressortir votre moteur de recherche. Pour chaque requête, nous avons également reporté les performances du moteur actuel (colonne position, qui renseigne la position 1,2,3,4 ou 5 du contenu idéal dans le moteur actuel et -1 si le moteur de recherche n'a pas trouvé le contenu dans le top 5 affiché actuellement sur le site),
- un script python de manière à évaluer le top5, top3 et top1 de votre algorithme, sur ces 20 requêtes, et son évolution tout au long du week-end,
- un interface web qui sera opérationnelle dimanche et permettant d'évaluer votre algorithme final sur 20 requêtes supplémentaires, disponible à l'adresse suivante http://51.38.39.210:8502/

Bien sûr, rien ne vaut un outil de démonstration pour attester de la pertinence d'un moteur de recherche ! Vous pouvez vous-même créer vos requêtes et tester votre algorithme sur des questions que vous vous posez !

## Auteurs
* **GreenAI UPPA** _alias_ [@GreenAI-UPPA](https://github.com/GreenAI-Uppa/)


## License
Ce projet est sous [Licence Creative Commons Attribution - Pas d'Utilisation Commerciale - Pas de Modification 4.0 International](http://creativecommons.org/licenses/by-nc-nd/4.0/).

