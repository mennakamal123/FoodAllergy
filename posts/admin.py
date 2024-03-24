from django.contrib import admin
from .models import Post, Comment

admin.site.register(Post)
admin.site.register(Comment)

# class PostAdmin(admin.ModelAdmin):
#     search_fields = ['allergy__arabicName', 'allergy__englishName']

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         search_term = request.GET.get('q')
#         if search_term:
#             qs = qs.filter(allergy__arabicName__icontains=search_term) | qs.filter(allergy__englishName__icontains=search_term)
#         return qs

# admin.site.register(Post, PostAdmin)
