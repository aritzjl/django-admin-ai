# Django Admin AI
---------------

An AI-powered enhancement for Django Admin that integrates artificial intelligence 
into the admin interface. This package provides utilities for AI-assisted data processing, 
automatic form population, intelligent suggestions, and more.

Key Features:
- Automated field population in Django models using AI

pip install django-admin-ai

en settings.py de el proyecto añadir
- import django_admin_ai y import os
- INSTALLED APPS -> 'django_admin_ai'
- TEMPLATES -> DIRS -> [os.path.join(BASE_DIR, 'templates/'),  
                        os.path.join(os.path.dirname(django_admin_ai.__file__), 'templates'),
                        ]
- DJANGO_ADMIN_AI_CONFIG = {
                            "openai_api_key": "<YOUR_OPENAI_API_KEY>"
                            }
- 
a urls.py del proyecto 
-ulrpatterns = [
                path('', include('django_admin_ai.urls'))
                ]

en admin.py de tu app por cada clase de tablas 
- ai_import = True