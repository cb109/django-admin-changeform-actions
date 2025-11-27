from typing import Callable, List, Optional, Tuple

from django.template import Template
from django.template.context import ContextDict
from django.urls import reverse


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
        return reverse("run_admin_changeform_action")

    def get_changeform_actions_dropdown(self, context) -> str:
        """Return HTML to run custom admin actions on the current object."""

        actions: List[Tuple[Callable, str, str]] = [
            (action, name, label)
            for (action, name, label) in self._get_base_actions()
            if name != "delete_selected"  # Skip the default delete action.
        ]
        if not actions:
            return ""

        opts: dict = self.model._meta
        app_label: str = opts.app_label
        model_name: str = opts.model_name

        object_id: Optional[int] = None
        for thing in context:
            if isinstance(thing, ContextDict):
                if "object_id" in thing:
                    object_id = thing["object_id"]
                    break
        if not object_id:
            return ""

        def make_option_html_for_action(action_name: str, action_label: str) -> str:
            return f"""
              <option value="{action_name}">{action_label}</option>
            """

        options_html: str = """
          <option value="" selected>---------</option>
        """
        for _, action_name, action_label in actions:
            options_html += make_option_html_for_action(action_name, action_label)

        template_html: str = f"""
          <li style="margin-left: 15px">
            <form
              action="{self.get_form_action_url()}"
              method="post"
            >
              {{% csrf_token %}}
              <input type="hidden" name="app_label" value="{app_label}">
              <input type="hidden" name="model_name" value="{model_name}">
              <input type="hidden" name="pk" value="{object_id}">
              <label>
                Aktion:
                <select
                  name="action"
                  style="
                    max-width: 240px;
                    margin: 0;
                    margin-left: 8px;
                    margin-right: 2px;
                  "
                 >
                  {options_html}
                </select>
                <button
                  type="submit"
                  onclick="this.disabled = true; this.form.submit();"
                  class="button"
                  style="
                    height: 30px;
                    padding: 4px 8px;
                    margin: 0;
                  "
                >
                  Los
                </button>
              </label>
            </form>
          </li>
        """
        return Template(template_html).render(context)
        return Template(template_html).render(context)
        return Template(template_html).render(context)
