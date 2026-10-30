import django
from django.apps import apps


def test_supported_django_version_is_locked() -> None:
    assert django.get_version() == "6.1.2"


def test_minimal_core_app_is_registered() -> None:
    assert apps.get_app_config("core").name == "apps.core"


def test_later_domain_apps_are_not_scaffolded() -> None:
    registered_apps = {config.name for config in apps.get_app_configs()}
    assert not registered_apps.intersection({"apps.tenants", "apps.users", "apps.audit"})
