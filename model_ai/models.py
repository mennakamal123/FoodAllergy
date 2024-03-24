# from django.db import models
# from database.models import Category

# class ImageClassification(models.Model):
#     image = models.ImageField(upload_to='images/')
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     result = models.CharField(max_length=500)

#     def __str__(self):
#         return f"{self.image.name} - {self.category.arabicName}"
