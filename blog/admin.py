from django.contrib import admin
from .models import Posts

# Register your models here.

class PostsAdmin(admin.ModelAdmin):
    field_sets=[
        ('Author',{'fields':['author_id']}),
        ('Posts_details',{'fields':['title','content','date_posted']}),
    ]
    list_display=['author','title','date_posted']
    list_filter=['date_posted']
    search_fields=['title']


admin.site.register(Posts,PostsAdmin)
