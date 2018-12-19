from django.db import models

# Create your models here.
class comments(models.Model):
	topic=models.CharField(max_length=200)
	comment=models.CharField(max_length=1000)
	def __str__(self):
		return self.comment
class logo(models.Model):
	image=models.ImageField(upload_to='images')
class wordcloud(models.Model):
	image=models.ImageField(upload_to='images')
class sentiment(models.Model):
	image=models.ImageField(upload_to='images')