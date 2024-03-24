from django.contrib import admin
from . import models
from .models import Allergy,Food
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
 
    search_fields = [
        "food__arabicName",
        "food__englishName",
        "allegry__arabicName",
        "allergy__englishName",
    ]

    filterset_fields = [
        "food__arabicName",
        "food__englishName",
        "allegry__arabicName",
        "allergy__englishName",
    ]
    

admin.site.register(models.Category, CategoryAdmin)

class FoodAllergyAdmin(admin.ModelAdmin):

    search_fields = [
        "arabicDescription",
        "englishDescription",
        "arabicName",
        "englishName",
        "arabicSymptoms",
        "englishSymptoms",
        "arabicProtection",
        "englishProtection",
    ]
    filterset_fields = [
        "arabicName",
        "englishName",
        "arabicSymptoms",
        "englishSymptoms",
        "arabicProtection",
        "englishProtection",
    ]

admin.site.register(models.FoodAllergy, FoodAllergyAdmin)

class MiniFoodAllergyAdmin(admin.ModelAdmin):
    search_fields = [
        "arabicName",
        "englishName",
    ]

    filterset_fields = [
        "arabicName",
        "englishName",
    ]
admin.site.register(models.MiniFoodAllergy, MiniFoodAllergyAdmin)

admin.site.register(Allergy)
admin.site.register(Food)