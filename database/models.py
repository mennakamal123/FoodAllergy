from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
class Food(models.Model):
    arabicName = models.CharField(max_length=500, verbose_name=_("Arabic name"))
    englishName = models.CharField(max_length=500, verbose_name=_("English name"))

    def __str__(self):
        return f"{self.arabicName} - {self.englishName}"


class Allergy(models.Model):
    arabicName = models.CharField(max_length=500, verbose_name=_("Arabic name"))
    englishName = models.CharField(max_length=500, verbose_name=_("English name"))
    
    def __str__(self):
        return f"{self.arabicName} - {self.englishName}"
    
   

class Category(models.Model):
    arabicName = models.CharField(max_length=500, verbose_name=_("Arabic name"))
    englishName = models.CharField(max_length=500, verbose_name=_("English name"))
    food = models.ManyToManyField("Food")
    allergy = models.ManyToManyField("Allergy")

    def __str__(self):
        return f"{self.arabicName} - {self.englishName}"

class FoodAllergy(models.Model):
    allergy_pic = models.ImageField(
        blank=True,
        null=True,
        upload_to="Allergy_pics",
    )
    arabicDescription = models.CharField(max_length=500, verbose_name=_("Arabic description"))
    englishDescription = models.CharField(max_length=500, verbose_name=_("English description"))
    arabicName = models.CharField(max_length=500, verbose_name=_("Arabic name"))
    englishName = models.CharField(max_length=500, verbose_name=_("English name"))
    arabicSymptoms = models.CharField(max_length=500, verbose_name=_("Arabic symptoms"))
    englishSymptoms = models.CharField(max_length=500, verbose_name=_("English symptoms"))
    arabicProtection = models.CharField(max_length=500, verbose_name=_("Arabic protection"))
    englishProtection = models.CharField(max_length=500, verbose_name=_("English protection"))

    def __str__(self):
        return f"{self.arabicName} - {self.englishName}"

class MiniFoodAllergy(models.Model):
    mini_allergy_pic = models.ImageField(
        blank=True,
        null=True,
        upload_to="miniAllergy_pics",
    )
    foodallergy = models.ForeignKey(FoodAllergy, on_delete=models.CASCADE, related_name='mini_food_allergies')
    arabicName = models.CharField(max_length=500, verbose_name=_("Arabic name"))
    englishName = models.CharField(max_length=500, verbose_name=_("English name"))
    
    def __str__(self):
        return f"{self.arabicName} - {self.englishName}"

# class Food(models.Model):
#     foodName = models.CharField(max_length=500)
    

#     def __str__(self):
#         return self.foodName


# class Allergy(models.Model):
#     allergyName = models.CharField(max_length=500)

#     def __str__(self):
#         return self.allergyName
    
    
    

# class Category(models.Model):
#     categoryName = models.CharField(max_length=500)
#     food = models.ManyToManyField("Food")
#     allergy = models.ManyToManyField("Allergy") 

#     def __str__(self):
#         return self.categoryName

# class FoodAllergy(models.Model):
#     allergy_pic = models.ImageField(
#         blank=True,
#         null=True,
#         upload_to="Allergy_pics",
#     )
#     foodallergyDescription = models.CharField(max_length=500)
#     foodallergyName = models.CharField(max_length=500)
#     foodallergySymptoms = models.CharField(max_length=500)
#     foodallergyProtection = models.CharField(max_length=500)

#     def __str__(self):
#         return self.foodallergyName