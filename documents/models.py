from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField()

    def __str__(self):
        return f'{self.title}'
