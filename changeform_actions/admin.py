from typing import Optional

from django.template.context import ContextDict
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import ActionForm

RUN_ACTION_URL: str = "run_admin_changeform_action"
DEFAULT_DELETE_ACTION_NAME: str = "delete_selected"


class ChangeFormActionsMixin:
    """Add support to run custom admin actions on the changeform page.

    This is handy as it allows to run custom actions on a single object
    instead of having to go back to the changelist page and select the
    desired one object there.

    Django's actions are not really made to be used outside of the
    changelist page, which is why this feature here is somewhat of a
    hack. It consists of the following:

    This mixin for a ModelAdmin to get the HTML for a dropdown:

      admin:ChangeFormActionsMixin

    A template tag to inject that dropdown into the changeform page:

      templatetags:get_changeform_actions_dropdown()

    A view to handle the dropdown submission and run the action:

      views:run_action_for_model_instance()

    We are bypassing the builtin actions handling, which expects a POST
    request against the ModelAdmin's changelist view including a
    selection of objects to act upon and an index for the selected
    action. Instead we pass any needed information as POST to our view,
    which then figures out which ModelAdmin instance to fetch from the
    admin.site registry and which action method to run on it against the
    current object/instance.

    """

    def get_form_action_url(self) -> str:
        return reverse(RUN_ACTION_URL)

    def get_changeform_actions_dropdown(self, request, context) -> str:
        """Return HTML to run custom admin actions on the current object."""

        opts: dict = self.model._meta
        app_label: str = opts.app_label
        model_name: str = opts.model_name

        object_id: Optional[int] = None
        for thing in context:
            if not isinstance(thing, ContextDict):
                continue
            if "object_id" in thing:
                object_id = thing["object_id"]
                break
        if not object_id:
            return ""

        action_form = ActionForm(auto_id=None)
        action_form.fields["action"].choices = [
            (name, label)
            for (name, label) in self.get_action_choices(request)
            if name != DEFAULT_DELETE_ACTION_NAME
        ]

        return render_to_string(
            "admin/actions_for_changeform.html",
            request=request,
            context={
                "action_form_url": self.get_form_action_url(),
                "action_form": action_form,
                "app_label": app_label,
                "model_name": model_name,
                "object_id": object_id,
            },
        )
