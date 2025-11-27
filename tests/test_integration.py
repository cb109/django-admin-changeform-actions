from django.conf import settings
from django.urls import resolve, reverse


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
