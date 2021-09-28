from django.db import models
from django.contrib.postgres.fields import ArrayField

class Banks(models.Model):
    number = models.IntegerField(verbose_name='Регистрационный номер', blank=True)
    title = models.CharField(verbose_name='Название банка', max_length=500, blank=True)
    urls = ArrayField(models.CharField(max_length=100))
    class Meta:
        verbose_name = 'Банк'
        verbose_name_plural = 'Банки'

