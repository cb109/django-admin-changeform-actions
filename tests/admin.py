from django import admin

from changeform_actions import ChangeFormActionsMixin


class MyModelAdmin(ChangeFormActionsMixin, admin.ModelAdmin):
    actions = ["my_custom_action"]

    def my_custom_action(self, request, obj):
        pass
