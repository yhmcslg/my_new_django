from django.contrib import admin
from app001.models import Publisher,Author,Book,Web_Console,Account
# Register your models here.


class PublisherAdmin(admin.ModelAdmin):
    pass

class AuthorAdmin(admin.ModelAdmin):
    pass

class BookAdmin(admin.ModelAdmin):
    list_display  = ['title','publisher','publication_date']
    fields = ['authors','publisher','publication_date','title']
    search_fields = ['publisher__name','title']
    list_filter = ['publication_date']
    date_hierarchy = 'publication_date'
    filter_vertical = ['authors']
    raw_id_fields = ['publisher']

class Web_ConsoleAdmin(admin.ModelAdmin):
    list_display = ['HostName','IP','http']

class AccountAdmin(admin.ModelAdmin):
    list_display = ['username','password']


admin.site.register(Publisher,PublisherAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(Web_Console,Web_ConsoleAdmin)
admin.site.register(Account,AccountAdmin)
