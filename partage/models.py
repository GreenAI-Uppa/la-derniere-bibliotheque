import datetime

from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

class Author(models.Model):
    nom = models.CharField(max_length=200)
    profession = models.CharField(max_length=200)
    organisation = models.CharField(max_length=200)
    def __str__(self):
        return self.nom

class Tag(models.Model):
    intitule = models.CharField(max_length=50)
    def __str__(self):
        return self.intitule

class Source(models.Model):
    auteur = models.ManyToManyField(Author)
    titre = models.CharField(max_length=200)
    def __str__(self):
        return self.titre

class Content(models.Model):
    text = models.TextField()
    text_game = models.TextField(blank=True)
    is_easy = models.BooleanField(blank=True, default=False)
    tag = models.ManyToManyField(Tag)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date de publication')
    def __str__(self):
        return self.text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    history = HistoricalRecords()

class Resultat_jeu1(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    occurence = models.IntegerField(blank=True)
    bonne_reponse = models.IntegerField(blank=True)
    def __str__(self):
        return str(self.content.id)

class Resultat_jeu2(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    occurence = models.IntegerField(blank=True)
    bonne_reponse = models.IntegerField(blank=True)
    def __str__(self):
        return str(self.content.id)
