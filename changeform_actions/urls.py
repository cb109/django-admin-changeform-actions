from django.urls import path

from . import views

urlpatterns = [
    path(
        "django-admin-changeform-actions/run",
        views.run_action_for_model_instance,
        name="run_admin_changeform_action",
    ),
]
