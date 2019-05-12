from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from PIL import Image



class Post(models.Model):
    title = models.CharField(max_length=100) #titulo tem maximo de 100 de caracteres
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #significa que cada post é 'tied to' a unico utilizador
    image = models.ImageField(default='default.jpg', upload_to='media')


#This is to printed out the post by the title
    def __str__(self): #defines how this thing turns into a string
    	return self.title

    def save(self, *args, **kwargs):
            super().save(*args, **kwargs)

            img = Image.open(self.image.path)

            if img.height > 150 or img.width >150:
                output_size = (150, 150)
                img.thumbnail(output_size)
                img.save(self.image.path)

#para so aparecer as primeiras 13 letras do conteudo na página principal
    def snippet(self):
    	return self.content[:13] + '...'

#para descobrir a localização de um post especifico
    def get_absolute_url(self):
    	return reverse('post-detail', kwargs={'pk': self.pk})
