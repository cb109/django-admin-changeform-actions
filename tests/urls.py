from django.urls import include, path

urlpatterns = [
    path("", include("changeform_actions.urls")),
]
