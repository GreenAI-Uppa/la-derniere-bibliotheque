from time import time
from django.shortcuts import render
from .models import Content
from .models import Tag
from .models import Author
from .models import Source
from . import recherche
import random
import json
import fasttext
from sklearn.manifold import TSNE
import numpy as np
from django.db import connection
from scipy.spatial import distance
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import umap
from django.template import RequestContext

fasttext.FastText.eprint = lambda x: None

############ Variables très utiles ############
content_list = Content.objects.all() # liste de tous les contenus
###############################################



############ Construction du graphe index.html ############
def all_vectors_content(model):
    matrice =[]
    # on vectorise chaque contenu et on les insère dans une matrice
    for i in range(Content.objects.count()):
        vec = recherche.embedding(content_list[i].text, model)
        matrice.append(vec)
    return matrice

# on charge le modèle, on effectue une réduction des vecteurs 
# grâce à umap et on stocke dans des variables
model = fasttext.load_model('models/model2.bin')
mat = all_vectors_content(model)
contenu_plan = umap.UMAP(n_neighbors=4).fit_transform(mat)
contenu_plan = np.array(contenu_plan)
data_x = []
data_y = []
data_x.append(contenu_plan[:,0])
data_y.append(contenu_plan[:,1])
################################################

## index() et next() renvoient tous les deux sur la même page html
## next() sert à afficher les contenus suivants


def index(request):
    content_list = Content.objects.all() # liste de tous les contenus
    content_http_list = Content.objects.filter(location__startswith="http") # liste de tous les contenus provenant de sites internet
    nmb_content = Content.objects.count() # nombre de contenu
    source_list = Source.objects.all() # liste de toutes les sources
    list_id = []
    for content in content_list:
        list_id.append(content.id)
    content_id = random.choice(list_id)
    texte = Content.objects.get(id=content_id) # contenu aléatoire parmi tous
    content_id_suivant = random.choice(list_id) # un autre contenu aléatoire
    # on stocke tous les id pour la création du graphe
    var_reconnaissance = 'reconnaissance'
    context = {
        'content_list': content_list,
        'texte': texte,
        'content_id_suivant': content_id_suivant,
        'content_http_list': content_http_list,
        'source_list': source_list,
        'data_x': data_x,
        'data_y': data_y,
        'var_reconnaissance': var_reconnaissance,
        'content_id': content_id,  
    }
    return render(request, 'partage/index.html', context)

def next(request, content_id):
    content_list = Content.objects.all() # liste de tous les contenus
    content_http_list = Content.objects.filter(location__startswith="http") # liste de tous les contenus provenant de sites internet
    nmb_content = Content.objects.count()
    source_list = Source.objects.all() # liste de toutes les sources
    texte = Content.objects.get(id=content_id)
    list_id = []
    for content in content_list:
        list_id.append(content.id)
    content_id_suivant = random.choice(list_id)
    context = {
        'content_id_suivant': content_id_suivant,
        'content_list': content_list,
        'texte': texte,
        'content_http_list': content_http_list,
        'data_x': data_x,
        'data_y': data_y,
        'source_list': source_list,
        'content_id': content_id,
    }
    return render(request, 'partage/index.html', context)

## tags() permet d'afficher tous les tags

tag_list = Tag.objects.all() # tous les tags de la bdd
occurence_tag = []
for tag in tag_list:
    i = 0
    for content in content_list:
        for t in content.tag.all():
            if t == tag:
                i = i+1
    occurence_tag.append(i)  

def tags(request):
    tag_list = Tag.objects.all() # tous les tags de la bdd
    # on calcule les occurences de chaque tag
    
    context = {
        'tag_list': tag_list,
        'occurence_tag': occurence_tag,
    }
    return render(request, 'partage/tags.html', context)

## author() permet d'afficher un certain auteur et ses informations

def author(request, author_name):
    source_list = Source.objects.all() # liste de toutes les sources
    auteur = Author.objects.filter(nom=author_name) # liste de tous les auteurs
    content_http_list = Content.objects.filter(location__startswith="http") # liste de tous les contenus provenant de sites internet
    context = {
        'source': source_list,
        'auteur': auteur,
        'content_http_list': content_http_list,
    }
    return render(request, 'partage/author.html', context)

## tag_detail() permet d'afficher tous les contenus d'un certain tag

def tag_detail(request, letag):
    content_list = Content.objects.order_by('?')
    content_http_list = Content.objects.filter(location__startswith="http") # liste de tous les contenus provenant de sites internet
    context = {
        'content_list': content_list,
        'letag': letag,
        'content_http_list': content_http_list,

    }
    return render(request, 'partage/leTag.html', context)

## allsources() permet d'afficher toutes les sources

def allsources(request):
    source_list = Source.objects.all() # liste de toutes les sources
    allsources = 'allsources'
    content_http_list = Content.objects.filter(location__startswith="http") # liste de tous les contenus provenant de sites internet
    context = {
        'source_list': source_list,
        'content_http_list': content_http_list,
        'allsources': allsources,
    }
    return render(request, 'partage/sources.html', context)

## source() permet d'afficher tous les contenus d'une certaine source

def source(request, source):
    content_list = Content.objects.all() # liste de tous les contenus
    content_http_list = Content.objects.filter(location__startswith="http") # liste de tous les contenus provenant de sites internet
    oneSource = 'oneSource'
    context = {
        'content_list': content_list,
        'source': source,
        'content_http_list': content_http_list,
        'oneSource': oneSource,
    }
    return render(request, 'partage/sources.html', context)

## contribute() permet d'afficher la page des contributeurs

def contribute(request):
    content_list = Content.objects.all() # liste de tous les contenus
    content_http_list = Content.objects.filter(location__startswith="http") # liste de tous les contenus provenant de sites internet
    ## c'est un peu le bordel ici ^^
    # Pour chaque utilisateur, on compte le nombre de contenus rentré dans la bdd
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM partage_historicalcontent WHERE history_user_id = 3 AND history_type='+'")
        row1 = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM partage_historicalcontent WHERE history_user_id = 3 AND history_type='-'")
        row1_bis = cursor.fetchone()
        for i in row1:
            for j in row1_bis:
                count = i-j
                nombre_contenu_ntirel = int(count)
    # Ensuite, on selectionne les contenus en question pour les afficher
    with connection.cursor() as cursor:
        req = "SELECT id FROM partage_historicalcontent WHERE id NOT IN (SELECT id FROM partage_historicalcontent WHERE history_type='-') AND history_type='+' AND history_user_id=3"
        cursor.execute(req)
        row11 = cursor.fetchall()
        if row11:
            contenu_ntirel = row11
            contenu_ntirel.reverse()
        else:
            contenu_ntirel = 'Pas de contenu'

    # même procédé
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM partage_historicalcontent WHERE history_user_id = 8 AND history_type='+'")
        row2 = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM partage_historicalcontent WHERE history_user_id = 8 AND history_type='-'")
        row2_bis = cursor.fetchone()
        for i in row2:
            for j in row2_bis:
                count = i-j
                nombre_contenu_sloustau = int(count)
    with connection.cursor() as cursor:
        req = "SELECT id FROM partage_historicalcontent WHERE id NOT IN (SELECT id FROM partage_historicalcontent WHERE history_type='-') AND history_type='+' AND history_user_id=8"
        cursor.execute(req)
        row21 = cursor.fetchall()
        if row21:
            contenu_sloustau = row21
            contenu_sloustau.reverse()
        else:
            contenu_sloustau = 'Pas de contenu'

    # même procédé
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM partage_historicalcontent WHERE history_user_id = 12 AND history_type='+'")
        row3 = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM partage_historicalcontent WHERE history_user_id = 12 AND history_type='-'")
        row3_bis = cursor.fetchone()
        for i in row3:
            for j in row3_bis:
                count = i-j
                nombre_contenu_slebeaud = int(count)
    with connection.cursor() as cursor:
        req = "SELECT id FROM partage_historicalcontent WHERE id NOT IN (SELECT id FROM partage_historicalcontent WHERE history_type='-') AND history_type='+' AND history_user_id=12"
        cursor.execute(req)
        row31 = cursor.fetchall()
        if row31:
            contenu_slebeaud = row31
            contenu_slebeaud.reverse()
        else:
            contenu_slebeaud = 'Pas de contenu'

    # même procédé
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM partage_historicalcontent WHERE history_user_id = 1 AND history_type='+'")
        row4 = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) FROM partage_historicalcontent WHERE history_user_id = 1 AND history_type='-'")
        row4_bis = cursor.fetchone()
        for i in row4:
            for j in row4_bis:
                count = i-j
                nombre_contenu_tpoupon = int(count)
    with connection.cursor() as cursor:
        req = "SELECT id FROM partage_historicalcontent WHERE id NOT IN (SELECT id FROM partage_historicalcontent WHERE history_type='-') AND history_type='+' AND history_user_id=1"
        cursor.execute(req)
        row41 = cursor.fetchall()
        if row41:
            contenu_tpoupon = row41
            contenu_tpoupon.reverse()
        else:
            contenu_tpoupon = 'Pas de contenu'

    tab_users = ['Nicolas','Sébastien','Simon', 'Thomas']
    tab_contenu = [contenu_ntirel, contenu_sloustau, contenu_slebeaud, contenu_tpoupon]
    sujet = "contribute"
    context = {
        'sujet': sujet,
        'content_list': content_list,
        'content_http_list': content_http_list,
        'tab_users': tab_users,
        'tab_contenu': tab_contenu,
        'nombre_contenu_ntirel': nombre_contenu_ntirel,
        'nombre_contenu_sloustau': nombre_contenu_sloustau,
        'nombre_contenu_slebeaud': nombre_contenu_slebeaud,
        'nombre_contenu_tpoupon': nombre_contenu_tpoupon,
    }
    return render(request, 'partage/more.html', context)

## leProjet() permet d'afficher la page explication sur le site

def leProjet(request):
    content_list = Content.objects.all() # liste de tous les contenus
    sujet = "leProjet"
    context = {
        'sujet': sujet,
        'content_list': content_list,
    }
    return render(request, 'partage/more.html', context)

## tous() permet d'afficher tous les contenus et pour y accéder il faut aller à l'url /partage/tous/

def tous(request):    
    content_list = Content.objects.all() # liste de tous les contenus
    content_http_list = Content.objects.filter(location__startswith="http") # liste de tous les contenus provenant de sites internet
    content_list_not_falsified = Content.objects.filter(text_game="") # contenu qui n'ont pas encore été traité pour les jeux
    content_list_falsified = Content.objects.exclude(text_game="") # contenu qui ont été traité pour les jeux
    context = {
        'content_list': content_list,
        'content_http_list': content_http_list,
        'content_list_not_falsified': content_list_not_falsified,
        'content_list_falsified': content_list_falsified,
    }
    return render(request, 'partage/tous.html', context)

############ Fonctions pour mettre les contenus dans un json ############
# Ces fonctions servent pour la mise en forme dans un json
def serialize_tag(content):
    list_tag = content.tag.all() # liste de tous les tags
    # On ajoute les tags d'un contenu dans un tableau que l'on retourne
    tab = []
    for tag in list_tag:
        tab.append(tag.intitule)
    return (tab)

def serialize(content):
    return{
        'text': content.text,
        'tag': serialize_tag(content),
        'source': content.source.titre,
    }
#########################################################################

## rechercher() permet d'afficher la page de recherche et de stocker tous les contenus dans un json

def rechercher(request):
    content_list = Content.objects.all() # liste de tous les contenus
    with open('partage/data.json', 'w') as mon_fichier:
        mon_fichier.write('{"Content":[')
        for content in content_list:
            if content.id != 8: # pour mettre des virgules avant chaque contenus sauf le premier (id du premier contenu = 8)
                mon_fichier.write(",")
            json.dump(serialize(content), mon_fichier)
        mon_fichier.write("]}") 
    context = {
        'content_list': content_list,
    }
    return render(request, 'partage/rechercher.html', context)

## rechercheSentence() permet d'afficher les résultats de la recherche
def rechercheSentence(request, sentence):
    content_list = Content.objects.all() # liste de tous les contenus
    content_http_list = Content.objects.filter(location__startswith="http") # liste de tous les contenus provenant de sites internet
    # On charge tous les contenus que l'on met dans la variable contents
    with open('partage/data.json', 'r') as json_file:
        data = json.load(json_file)
    contents = data['Content']
    n_voisin = 5 # nombre de voisins les plus proches à afficher
    tab = recherche.voisins_sentence(sentence, contents, model, n_voisin) # on utilise la fonction voisins_sentence()
    distances = tab[1][0] # on récupère les distances entre les voisins et la phrase de départ
    # on récupère les plus proches voisins dans tab_content
    tab_content = []
    for i in tab[0]:
        tab_content.append(content_list[int(i)])
    context = {
        'sentence': sentence,
        'tab_content': tab_content,
        'content_list': content_list,
        'content_http_list': content_http_list,
        'distance': distances,
    }
    return render(request, 'partage/rechercher.html', context)

## jeu() est la page d'accueil des jeux

nombre_question = 10 #Modifier cette variable et tout changera automatiquement

def jeu(request):
    objet_inutile = 'test' # permet de tout faire sur une seule page html
    with connection.cursor() as cursor:
        # on récupère les 10 meilleurs score (chaque joueur ne peut avoir qu'un seul score dans le top 10)
        req = "SELECT pseudo, score FROM score_game as s WHERE score=(SELECT MAX(score) FROM score_game as g WHERE g.pseudo=s.pseudo LIMIT 1) GROUP BY pseudo ORDER BY score DESC"
        cursor.execute(req)
        pseudo_score_1 = cursor.fetchall()
        req = "SELECT pseudo, score FROM score_game_2 as s WHERE score=(SELECT MAX(score) FROM score_game_2 as g WHERE g.pseudo=s.pseudo LIMIT 1) GROUP BY pseudo ORDER BY score DESC"
        cursor.execute(req)
        pseudo_score_2 = cursor.fetchall()
    context = {
        'objet_inutile': objet_inutile,
        'nombre_question': nombre_question,
        'pseudo_score_1': pseudo_score_1,
        'pseudo_score_2': pseudo_score_2,
    }
    return render(request, 'partage/jouer.html', context)

## jouer() permet le déroulement du jeu n°1

def jouer(request):
    content_http_list = Content.objects.filter(location__startswith="http") # liste de tous les contenus provenant de sites internet
    # on sélectionne les contenus qui ont été falsifié et on les met dans tab_content_exploitable
    tab_content_exploitable = []
    for content in content_list:
        if content.text_game != '':
            tab_content_exploitable.append(content)
    # tant que la taille du tableau n'est pas égale à 10
    # on y ajoute des contenus aléatoirement depuis tab_content_exploitable
    # (pour éviter d'avoir un ordre dans ce qui est affiché)
    tab_content_utilise = []
    while len(tab_content_utilise) != nombre_question:
        rand = random.randrange(0, len(tab_content_exploitable))
        tab_content_utilise.append(tab_content_exploitable[rand])
        tab_content_exploitable.remove(tab_content_exploitable[rand])
    # On remplit un tableau de 0 et de 1 pour savoir si le contenu vrai sera à gauche ou à droite
    tab_affichage_rand = []
    while len(tab_affichage_rand) != nombre_question:
        affichage_rand = random.randrange(0,2)
        tab_affichage_rand.append(affichage_rand)
    context = {
        'tab_content_utilise': tab_content_utilise,
        'tab_affichage_rand': tab_affichage_rand,
        'content_http_list': content_http_list,
        'nombre_question': nombre_question,
    }
    return render(request, 'partage/jouer.html', context)

## jouer2() permet le déroulement du jeu n°2

def jouer2(request):
    content_http_list = Content.objects.filter(location__startswith="http") # liste de tous les contenus provenant de sites internet
    # le procédé est le même que pour le jeu n°1
    tab_content_exploitable = []
    for content in content_list:
        if content.text_game != '':
            tab_content_exploitable.append(content)
    tab_content_utilise = []
    while len(tab_content_utilise) != nombre_question:
        rand = random.randrange(0, len(tab_content_exploitable))
        tab_content_utilise.append(tab_content_exploitable[rand])
        tab_content_exploitable.remove(tab_content_exploitable[rand])
    tab_affichage_rand = []
    while len(tab_affichage_rand) != nombre_question:
        affichage_rand = random.randrange(0,2)
        tab_affichage_rand.append(affichage_rand)
    context = {
        'tab_content_utilise': tab_content_utilise,
        'tab_affichage_rand': tab_affichage_rand,
        'content_http_list': content_http_list,
        'nombre_question': nombre_question,
    }
    return render(request, 'partage/jouer2.html', context)

## envoyer() permet de stocker les scores et d'afficher le tableau des meilleurs scores pour le jeu n°1

def envoyer(request):
    pseudo = request.POST.get('pseudo') # on récupère le pseudo envoyer par la méthode POST
    score = request.POST.get('score') # on récupère le score envoyer par la méthode POST
    if isinstance(pseudo, str) and (isinstance(int(score), int)) and (int(score) >= 0) and (int(score) <= 10) and (len(pseudo) < 20) and (len(pseudo.replace(' ', ''))>0):
        variable_verif = 0
        for i in range(nombre_question):
            reponse = request.POST.get(f'score_{i}') # on récupère le résultat (true or false)
            if reponse == "true":
                variable_verif = variable_verif + 1
        if variable_verif == int(score) :
            ## Ici on va stocker le score de réussite par contenu (pour savoir la difficulté d'un contenu)
            # on entre dans la bdd
            with connection.cursor() as cursor:
                for i in range(nombre_question): # il y a 10 questions
                    reponse = request.POST.get(f'score_{i}') # on récupère le résultat (true or false)
                    id_content = request.POST.get(f'id_{i}') # on récupère l'id du contenu
                    if reponse == "true":
                        # Si le contenu a déja un score enregistré on le met à jour
                        req = f'UPDATE partage_resultat_jeu1 SET occurence = occurence + 1, bonne_reponse = bonne_reponse + 1 WHERE content_id = "{id_content}";'
                        cursor.execute(req)
                        # Sinon on créé une ligne dans la bdd
                        req = f'INSERT INTO partage_resultat_jeu1(content_id, occurence, bonne_reponse) SELECT "{id_content}", "1", "1" WHERE NOT EXISTS (SELECT content_id FROM partage_resultat_jeu1 WHERE content_id="{id_content}");'
                        cursor.execute(req)
                    if reponse == "false":
                        # Si le contenu a déja un score enregistré on le met à jour
                        req = f'UPDATE partage_resultat_jeu1 SET occurence = occurence + 1 WHERE content_id = "{id_content}";'
                        cursor.execute(req)
                        # Sinon on créé une ligne dans la bdd
                        req = f'INSERT INTO partage_resultat_jeu1(content_id, occurence, bonne_reponse) SELECT "{id_content}", "1", "0" WHERE NOT EXISTS (SELECT content_id FROM partage_resultat_jeu1 WHERE content_id="{id_content}");'
                        cursor.execute(req)
                # on y insère le pseudo et score
                req = f'INSERT INTO score_game VALUES ("{pseudo}", "{score}")'
                cursor.execute(req)
    # on entre dans la bdd
    with connection.cursor() as cursor:
        # on récupère les 10 meilleurs score (chaque joueur ne peut avoir qu'un seul score dans le top 10)
        req = "SELECT pseudo, score FROM score_game as s WHERE score=(SELECT MAX(score) FROM score_game as g WHERE g.pseudo=s.pseudo LIMIT 1) GROUP BY pseudo ORDER BY score DESC LIMIT 10"
        cursor.execute(req)
        pseudo_score = cursor.fetchall()
    context = {
        'pseudo_score': pseudo_score,
    }
    return render(request, 'partage/jouer.html', context)

## envoyer2() permet de stocker les scores et d'afficher le tableau des meilleurs scores pour le jeu n°2

def envoyer2(request):
    # le procédé est le même que pour le jeu n°1
    pseudo = request.POST.get('pseudo')
    score = request.POST.get('score')
    if isinstance(pseudo, str) and (isinstance(int(score), int)) and (int(score) >= 0) and (int(score) <= 10) and (len(pseudo) < 20) and (len(pseudo.replace(' ', ''))>0):
        variable_verif = 0
        for i in range(nombre_question):
            reponse = request.POST.get(f'score_{i}') # on récupère le résultat (true or false)
            if reponse == "true":
                variable_verif = variable_verif + 1
        if variable_verif == int(score) :
            ## Ici on va stocker le score de réussite par contenu (pour savoir la difficulté d'un contenu)
            # on entre dans la bdd
            with connection.cursor() as cursor:
                for i in range(nombre_question): # il y a 10 questions
                    reponse = request.POST.get(f'score_{i}') # on récupère le résultat (true or false)
                    id_content = request.POST.get(f'id_{i}') # on récupère l'id du contenu
                    if reponse == "true":
                        # Si le contenu a déja un score enregistré on le met à jour
                        req = f'UPDATE partage_resultat_jeu2 SET occurence = occurence + 1, bonne_reponse = bonne_reponse + 1 WHERE content_id = "{id_content}";'
                        cursor.execute(req)
                        # Sinon on créé une ligne dans la bdd
                        req = f'INSERT INTO partage_resultat_jeu2(content_id, occurence, bonne_reponse) SELECT "{id_content}", "1", "1" WHERE NOT EXISTS (SELECT content_id FROM partage_resultat_jeu2 WHERE content_id="{id_content}");'
                        cursor.execute(req)
                    if reponse == "false":
                        # Si le contenu a déja un score enregistré on le met à jour
                        req = f'UPDATE partage_resultat_jeu2 SET occurence = occurence + 1 WHERE content_id = "{id_content}";'
                        cursor.execute(req)
                        # Sinon on créé une ligne dans la bdd
                        req = f'INSERT INTO partage_resultat_jeu2(content_id, occurence, bonne_reponse) SELECT "{id_content}", "1", "0" WHERE NOT EXISTS (SELECT content_id FROM partage_resultat_jeu2 WHERE content_id="{id_content}");'
                        cursor.execute(req)
                # on y insère le pseudo et score
                req = f'INSERT INTO score_game_2 VALUES ("{pseudo}", "{score}")'
                cursor.execute(req)
    # on entre dans la bdd
    with connection.cursor() as cursor:
        # on récupère les 10 meilleurs score (chaque joueur ne peut avoir qu'un seul score dans le top 10)
        req = "SELECT pseudo, score FROM score_game_2 as s WHERE score=(SELECT MAX(score) FROM score_game_2 as g WHERE g.pseudo=s.pseudo LIMIT 1) GROUP BY pseudo ORDER BY score DESC LIMIT 10"
        cursor.execute(req)
        pseudo_score = cursor.fetchall()
    context = {
        'pseudo_score': pseudo_score,
    }
    return render(request, 'partage/jouer2.html', context)
