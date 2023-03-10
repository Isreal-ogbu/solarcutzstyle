from django.contrib import admin
from phoneverificationapp.models import phonenumbermodel


class Admin_page_display(admin.ModelAdmin):
    list_display = ('owner', 'phonenumber', 'verifiednumber')
    search_fields = 'phonenumber'


admin.site.register(phonenumbermodel)
