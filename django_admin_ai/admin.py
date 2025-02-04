from django.contrib import admin
from django.urls import NoReverseMatch, path, reverse
from django.utils.safestring import mark_safe
from django.shortcuts import redirect

class AIAdminMixin:
    """
    Mixin to add the "AI Import" button in the Django admin panel.
    """
    def get_urls(self):
        urls = super().get_urls()
        ai_urls = [
            path(
                "ai-import/<uuid:object_id>/",
                self.admin_site.admin_view(self.ai_import_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_ai_import",
            ),
        ]
        return ai_urls + urls

    def ai_import_view(self, request, object_id):
        # Placeholder for the AI import logic
        self.message_user(request, "AI import feature coming soon!", level="info")
        return redirect(request.META.get("HTTP_REFERER", "admin:index"))

    def render_change_form(self, request, context, *args, **kwargs):
        response = super().render_change_form(request, context, *args, **kwargs)

        if getattr(self, "ai_import", False):
            obj = context.get("original")  # Get the current object

            opts = self.model._meta
            try:
                ai_import_url = reverse(
                    "admin_ai_import", args=[opts.app_label, opts.model_name]
                )
            except Exception as e:
                print(f"❌ Error in reverse(): {e}")
                ai_import_url = "#"

            # Pass the URL to the context
            context["ai_import_url"] = ai_import_url  

        return response
