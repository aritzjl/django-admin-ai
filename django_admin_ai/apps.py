from django.apps import AppConfig
from django.contrib import admin

class DjangoAdminAIConfig(AppConfig):
    name = "django_admin_ai"
    verbose_name = "Django Admin AI"

    def ready(self):
        from django_admin_ai.admin import AIAdminMixin
        
        # Make a copy of the elements in admin.site._registry
        registered_models = list(admin.site._registry.items())

        for model, model_admin in registered_models:
            if hasattr(model_admin, "ai_import") and model_admin.ai_import:
                admin.site.unregister(model)  # First, unregister the model
                new_admin_class = type(
                    f"{model.__name__}AIAdmin",
                    (AIAdminMixin, model_admin.__class__),
                    {"ai_import": True}  # Preserve the property
                )
                admin.site.register(model, new_admin_class)  # Register the new Admin class

        from django.conf import settings
        
        # Override the template directory
        if hasattr(settings, "TEMPLATES"):
            settings.TEMPLATES[0]["DIRS"].insert(0, "django_admin_ai/templates")
