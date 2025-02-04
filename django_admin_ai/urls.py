from django.urls import path
from .views import ai_import_view

urlpatterns = [
    path("ai-import/<str:app_label>/<str:model_name>//", ai_import_view, name="admin_ai_import"),
    
]