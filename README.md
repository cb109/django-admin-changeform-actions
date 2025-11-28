# django-admin-changeform-actions

Replicates the admin
[actions](https://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/)
dropdown (available on a model's `changelist` page) on each model
instance's `changeform` page.

Instead of targetting a selection the action will target the current
model instance only.

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

## Development Setup

This project uses [uv](https://docs.astral.sh/uv/) to handle python versions and dependencies.

```bash
uv sync
```

## Tests

```bash
uv run pytest
```

Run test matrix of different python versions VS different django versions:
```bash
uv run tox
```
