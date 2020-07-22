from django.contrib import admin
from .models import *

[admin.site.register(_) for _ in all_objects_to_be_added_in_adminpage]