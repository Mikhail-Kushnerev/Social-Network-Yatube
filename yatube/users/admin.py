from django.contrib import admin
from django.utils.safestring import mark_safe

# from .models import Profile


# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = (
#         'user',
#         'image_show'
#     )

#     def image_show(self, obj):
#         if obj.image:
#             return mark_safe(
#                 "<img src='{}' width='60' />".format(obj.image.url)
#             )
#         return "None"

#     image_show.__name__ = "Картинка"
