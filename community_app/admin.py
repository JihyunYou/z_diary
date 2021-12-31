from django.contrib import admin

from community_app.models import Subject


class SubjectAdmin(admin.ModelAdmin):
    model = Subject

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


admin.site.register(Subject, SubjectAdmin)
