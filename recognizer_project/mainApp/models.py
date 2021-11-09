from django.db import models
from django.contrib.postgres.fields import ArrayField


class Banks(models.Model):
    number = models.IntegerField(verbose_name='Регистрационный номер', blank=True)
    title = models.CharField(verbose_name='Название банка', max_length=500, blank=True)
    urls = ArrayField(models.CharField(max_length=1000))

    class Meta:
        verbose_name = 'Банк'
        verbose_name_plural = 'Банки'

    def __str__(self):
        return f'{self.title}'

class FakeUrls(models.Model):

    title = models.ForeignKey('Banks', verbose_name='Относится к банку', on_delete=models.CASCADE)
    url = models.CharField(verbose_name='URL', max_length=100, blank=True)
    colors = ArrayField(models.CharField(max_length=1000))

    class Meta:
        verbose_name = 'Фейковый url'
        verbose_name_plural = 'Фейковые url'

    def __str__(self):
        return f'Fake_{self.title}'