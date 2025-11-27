from django.apps import apps
from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_http_methods


@require_http_methods(("POST",))
def run_action_for_model_instance(request):
    """Run specified custom admin action on a model instance.

    This acts as a custom handler for our custom admin actions
    dropdown on a ModelAdmin's changeform page. The idea is to have the
    same outcome as selecting the model instance on the changelist page
    and executing the action there, just more conveniently from its
    changeform aka detail page.

    After running the action we redirect back to where we came from.

    For the corresponding ModelAdmin code, see:

        admin.common.ChangeFormActionsMixin

    """
    referer_url: str = request.META["HTTP_REFERER"]

    app_label: str = request.POST["app_label"]
    model_name: str = request.POST["model_name"]
    pk: int = int(request.POST["pk"])
    action_name: str = request.POST.get("action", "")

    if not action_name:
        # Probably submitted the default empty option, ignore.
        return HttpResponseRedirect(referer_url)

    model_cls: type = apps.get_model(app_label, model_name)
    queryset: QuerySet = model_cls.objects.filter(pk=pk)
    instance: object = model_cls.objects.get(pk=pk)

    model_admin: object = admin.site._registry[model_cls]
    for action, name, label in model_admin._get_base_actions():
        if name == action_name:
            action(model_admin, request, queryset)
            model_admin.message_user(
                request, f"Aktion '{label}' ausgeführt für: '{instance}'"
            )

    return HttpResponseRedirect(referer_url)
