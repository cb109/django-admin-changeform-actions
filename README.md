# django-admin-changeform-actions

Django's
[ModelAdmin.actions](https://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/)
are available only on a model's `changelist` page by default. This
package makes them available on the model's `changeform` page as well.

This allows to reuse custom admin actions on a specific model instance quickly.

## Installation

Install the package:

```bash
cd django-admin-changeform-actions/
pip install -e .
```

Modify your Django project like:

```py
# settings.py

INSTALLED_APPS = [
  "changeform_actions",
]
```

```py
# urls.py

urlpatterns = [
  path("", include("changeform_actions.urls"))
]
```

```py
# admin.py

from changeform_actions import ChangeFormActionsMixin

class MyModelAdmin(ChangeFormActionsMixin, admin.ModelAdmin):
    actions = [...]
```

## Tests

```bash
uv sync
uv run pytest .
```
