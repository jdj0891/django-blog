from django.contrib import admin
from blogging.models import Post, Category, Comment


class CategoryInline(admin.TabularInline):
    model = Category.post.through

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CategoryInline,
    ]

class CategoryAdmin(admin.ModelAdmin):
    exclude = ('post',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
