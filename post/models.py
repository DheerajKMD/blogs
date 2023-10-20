# cookbook/ingredients/models.py
from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    publish_date = models.CharField(max_length=200)    
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(
        Blog, related_name="Blog", on_delete=models.CASCADE
    )
    text = models.TextField()
    author = models.CharField(max_length=100)    

    def __str__(self):
        return self.author
    
    