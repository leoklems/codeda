from django.db import models

# Create your models here.

class Search(models.Model):
    search = models.CharField(max_length = 500, null = True)
    created = models.DateTimeField(auto_now = True)

    # when you want to control some of the displays, you use the class Meta
    def __str__(self):
        return  '{}'.format(self.search)
    class Meta:
        verbose_name_plural = "Searches"