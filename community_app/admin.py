from django.contrib import admin

from community_app.models import Category


class CategoryAdmin(admin.ModelAdmin):
    model = Category

    list_display = ('name', 'description')
    list_filter = ('name',)

    fieldsets = (
        ('카테고리', {'fields': ('name', 'description')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'description')}
         ),
    )


admin.site.register(Category, CategoryAdmin)
