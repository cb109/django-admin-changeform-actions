from django.contrib import admin

from changeform_actions import ChangeFormActionsMixin
from tests.models import MyModel


class MyModelAdmin(ChangeFormActionsMixin, admin.ModelAdmin):
    actions = ["my_custom_action"]

    def my_custom_action(self, request, obj):
        pass


admin.site.register(MyModel, MyModelAdmin)
