from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    # TODO: законспектировать
    image = models.ImageField(blank=True, default='default.png')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title   

    def snippet(self):
        return self.body[:30] + '...'
