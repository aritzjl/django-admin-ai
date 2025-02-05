# Django Admin AI
---------------

An AI-powered enhancement for Django Admin that integrates artificial intelligence 
into the admin interface. This package provides utilities for AI-assisted data processing, 
automatic form population, intelligent suggestions, and more.

Key Features:
- Automated field population in Django models using AI

### Installation
Prerequisites
- Python 3.8+ or later
- Django 3.0+ or later

To install the library, run the following on your terminal:<br>
 
```pip install django-admin-ai```

### Setup
On your __projects__ settings.py add the following:
- ```import django_admin_ai``` and ```import os```
- INSTALLED APPS → ```'django_admin_ai'```
- TEMPLATES → DIRS → ```[os.path.join(BASE_DIR, 'templates/'),  
                        os.path.join(os.path.dirname(django_admin_ai.__file__), 'templates'),
                        ]```
-  ```DJANGO_ADMIN_AI_CONFIG = {"openai_api_key": "<YOUR_OPENAI_API_KEY>"}```

On the urls.py of your __project__ add the next path:
- ```ulrpatterns = [ path('', include('django_admin_ai.urls'))]```

On the admin.py of your __app__, for each class that contains modals for the tables, add this:   
- ```ai_import = True```
