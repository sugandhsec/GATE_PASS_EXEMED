
from import_export import resources
from .models import *

class Rgp_entryResource(resources.ModelResource):
    class Meta:
        model = Rgp_entry

class Nrgp_entryResource(resources.ModelResource):
    class Meta:
        model = Nrgp_entry

class User_rgpResource(resources.ModelResource):
    class Meta:
        model = User_rgp

