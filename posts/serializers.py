from rest_framework import serializers
from .models import Post, Comment, ContactMessage
from django.contrib.contenttypes.models import ContentType

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    owner_profile_pic = serializers.ImageField(source='owner.profile_pic', read_only=True)

    def create(self, validated_data):
        # Check if the user is a doctor
        user = self.context['request'].user
        if user.is_doctor:
            validated_data['owner'] = user
            return super().create(validated_data)
        else:
            raise serializers.ValidationError("Only doctors can create comments")

    class Meta:
        model = Comment
        fields = '__all__'


# class PostSerializer(serializers.ModelSerializer):
#     owner = serializers.SlugRelatedField(slug_field='username',read_only=True)
#     comments = CommentSerializer(many=True, read_only=True, source='comment_set')
#     owner_profile_pic = serializers.ImageField(source='owner.profile_pic', read_only=True)
#     allergy_arabic_name = serializers.CharField(source='allergy.arabicName', read_only=True)
#     allergy_english_name = serializers.CharField(source='allergy.englishName', read_only=True)
#     is_liked = serializers.BooleanField(read_only=True)
#     class Meta:
#         model = Post
#         # fields = ['id','owner','comments','is_liked','title','image','created_at','updated_at']
#         fields = ['id','owner','comments','is_liked','title','image','created_at','updated_at','owner_profile_pic',
#                   "allergy_arabic_name","allergy_english_name", "likes"]

#         extra_kwargs = { 'likes':{'read_only':True}}


#     def get_is_liked(self, obj):
#         request = self.context.get('request')
#         if request and request.user.is_authenticated:
#             if request.user in obj.likes.all():
#                 return True
#         return False

class PostSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    owner_profile_pic = serializers.ImageField(source='owner.profile_pic', read_only=True)
    allergy_arabic_name = serializers.SerializerMethodField(read_only=True)
    allergy_english_name = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        # fields = ['id','owner','comments','is_liked','title','image','created_at','updated_at']
        fields = ['id','owner_name','owner','comments','is_liked','title','image','created_at','updated_at','owner_profile_pic',
                  "allergy_arabic_name","allergy_english_name", "likes",'allergy']

        extra_kwargs = {
            'likes':{'read_only':True},
            'allergy':{'write_only':True}
            }

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            if request.user in obj.likes.all():
                return True
        return False

    
    def get_allergy_arabic_name(self,obj):
        if obj.allergy:
            return obj.allergy.arabicName
        else:
            return None
    
    def get_allergy_english_name(self,obj):
        if obj.allergy:
            return obj.allergy.englishName
        else:
            return None
    
class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']
