from django.db import models

class NewsSource(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    source = models.ForeignKey(NewsSource, on_delete=models.CASCADE)
    publish_time = models.DateTimeField()
    url = models.URLField(unique=True)
    
    def __str__(self):
        return self.title
