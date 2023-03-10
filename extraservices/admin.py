from django.contrib import admin

# Register your models here.
from extraservices.models import idea_suggestionmodel, contact_supportmodel

admin.site.register(idea_suggestionmodel)
admin.site.register(contact_supportmodel)