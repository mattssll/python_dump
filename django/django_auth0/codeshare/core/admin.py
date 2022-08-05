# codeshare/core/admin.py
from django.contrib import admin
from .models import Post, Organization, Person
admin.site.register(Post)
admin.site.register(Organization)
admin.site.register(Person)