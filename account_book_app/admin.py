from django.contrib import admin

from account_book_app.models import Category, Account


class CategoryAdmin(admin.ModelAdmin):
    model = Category

    list_display = ('name', 'description', 'created_by')
    list_filter = ('name', 'created_by',)

    fieldsets = (
        ('카테고리', {'fields': ('name', 'description', 'created_by',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'description', 'created_by')}
         ),
    )


class AccountAdmin(admin.ModelAdmin):
    model = Account

    list_display = ('user_id', 'category_id', 'date', 'amount', 'description')
    list_filter = ('user_id', 'category_id',)

    fieldsets = (
        ('가계부', {'fields': ('user_id', 'category_id', 'date', 'amount', 'description', 'created_by',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id', 'category_id', 'date', 'amount', 'description', 'created_by')}
         ),
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Account, AccountAdmin)
