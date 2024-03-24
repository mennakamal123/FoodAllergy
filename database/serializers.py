from rest_framework import serializers
from .models import Allergy, Category, Food, FoodAllergy, MiniFoodAllergy
from cart.serializers import ProductSerializer
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = "__all__"


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = "__all__"


class AllergySerializer_(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Allergy
        fields = "__all__"
        
class CategorySerializer(serializers.ModelSerializer):
    food = serializers.SerializerMethodField()
    allegry = serializers.SerializerMethodField()
    class Meta:

        model = Category
        fields = "__all__"

    def get_food(self, obj):
        food = obj.food
        dataofFood = {"arabicName": food.arabicName, "englishName": food.englishName}
        return dataofFood

    def get_allergy(self, obj):
        allergy = obj.allergy
        dataofallergy = {
            "arabicName": allergy.arabicName,
            "englishName": allergy.englishName,
        }
        return dataofallergy
class CategorySerializer_(serializers.ModelSerializer):
    food = FoodSerializer(many=True)
    allergy = AllergySerializer(many=True)
    class Meta:

        model = Category
        fields = "__all__"
class FoodAllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodAllergy
        fields = "__all__"

    def get_foodallergy(self, obj):
        foodallegry = obj.foodallegry
        dataoffoodallegry = {
            "allergy_pic": foodallegry.allergy_pic,
            "arabicDescription": foodallegry.arabicDescription,
            "englishDescription": foodallegry.englishDescription,
            "arabicName": foodallegry.arabicName,
            "englishName": foodallegry.englishName,
            "arabicSymptoms": foodallegry.arabicSymptoms,
            "englishSymptoms": foodallegry.englishSymptoms,
            "arabicPrevention": foodallegry.arabicProtection,
            "englishPrevention": foodallegry.englishProtection,
        }
        return dataoffoodallegry
    
class MiniFoodAllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = MiniFoodAllergy
        fields = "__all__"

    def get_foodallergy(self, obj):
        minifoodallegry = obj.minifoodallegry
        dataofminifoodallegry = {
            "mini_allergy_pic": minifoodallegry.mini_allergy_pic,
            "arabicName": minifoodallegry.arabicName,
            "englishName": minifoodallegry.englishName,
        }
        return dataofminifoodallegry