from django.db import models

from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=500)
    author = models.ForeignKey(User)
    category = models.ForeignKey('Category')
    tags = models.ManyToManyField('Tag', blank=True)
    date = models.DateField(auto_now=True)

    class Meta:
        ordering = ('date',)

    def __unicode__(self):
        return '{0} - {1} | {2}'.format(self.title, self.date, self.category)


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name.title()


class Tag(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name.title()