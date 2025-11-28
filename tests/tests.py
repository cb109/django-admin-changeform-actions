import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client
from django.urls import resolve, reverse

from tests.models import MyModel


@pytest.mark.django_db
class TestIntegration:
    def test_app_installed(self):
        assert "changeform_actions" in settings.INSTALLED_APPS

    def test_urls_included(self):
        match = resolve(reverse("changeform_actions:run_admin_changeform_action"))
        assert match.app_name == "changeform_actions"
        assert match.url_name == "run_admin_changeform_action"

    def test_admin_mixin_importable(self):
        from changeform_actions import ChangeFormActionsMixin

        assert ChangeFormActionsMixin is not None

    def test_changeform_has_actions_dropdown(self):
        # Create superuser and log in
        User.objects.create_superuser("admin", "admin@example.com", "password")
        client = Client()
        client.login(username="admin", password="password")

        # Create a model instance
        instance = MyModel.objects.create(name="Test")

        # Get changeform page and check that the dropdown is present
        changeform_url = reverse("admin:tests_mymodel_change", args=[instance.pk])
        response = client.get(changeform_url)
        assert response.status_code == 200
        assert b'<select name="action"' in response.content
