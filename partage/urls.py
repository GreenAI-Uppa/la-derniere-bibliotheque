from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tags/', views.tags, name='tags'),
    path('next/<int:content_id>/', views.next, name='next'),
    path('author/<str:author_name>/', views.author, name="author"),
    path('<str:letag>/contenus/', views.tag_detail, name="tag_detail"),
    path('sources/allsources/', views.allsources, name="allsources"),
    path('sources/<str:source>/', views.source, name="source"),
    path('more/contribute/', views.contribute, name="contribute"),
    path('more/leProjet/', views.leProjet, name="grenAI"),
    path('tous/', views.tous, name="tous"),
    path('rechercher/', views.rechercher, name="rechercher"),
    path('rechercher/<str:sentence>/', views.rechercheSentence, name='rechercheSentence'),
    path('jeu/', views.jeu, name="jeu"),
    path('jouer/', views.jouer, name="jouer"),
    path('envoyer/', views.envoyer, name="envoyer"),
    path('jouer2/', views.jouer2, name="jouer2"),
    path('envoyer2/', views.envoyer2, name="envoyer2"),
]