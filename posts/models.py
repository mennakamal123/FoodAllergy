from django.db import models
from django.contrib.auth.models import User
from users.models import User, Doctor, Patient
from database.models import Allergy
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=500)
    image = models.ImageField( null=True, blank=True)
    allergy = models.ForeignKey(Allergy, related_name='posts', on_delete=models.PROTECT, null=True)
    owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name='likes',blank=True)
    def __str__(self):
        return self.title
  
    # class Meta:
    #     ordering = ['-created']

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.post.id)])
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.TextField(max_length=300)

    def __str__(self):
        return self.name
    