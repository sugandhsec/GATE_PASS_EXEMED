from import_export import resources

from django.contrib import admin

from myapp.resources import Rgp_entryResource , User_rgpResource  , Nrgp_entryResource
from .models import User_rgp,Rgp_entry,Nrgp_entry
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class Rgp_entryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = Rgp_entryResource

class Nrgp_entryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = Nrgp_entryResource


class user_rgpAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = User_rgpResource

# class logAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     resource_class = logResource
  

admin.site.register(User_rgp , user_rgpAdmin)
admin.site.register(Rgp_entry , Rgp_entryAdmin)
admin.site.register(Nrgp_entry , Nrgp_entryAdmin)

