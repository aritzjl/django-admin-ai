# Django Admin AI

An **AI-powered enhancement** for Django Admin that integrates artificial intelligence directly into the Django admin panel. This package provides utilities for **AI-assisted data processing, automatic form population, intelligent suggestions, and more**.

## 🚀 Key Features

✅ **AI-driven form population**: Automatically fill forms by extracting data from various document types (PDF, images, text files).  
✅ **Seamless Django Admin integration**: Enable AI-enhanced forms with a single line of code.  
✅ **Easy setup**: Minimal configuration required to get started.  

### 🔮 Future Enhancements (Planned Features)

🚀 **Voice input support**: Record audio directly in Django Admin and let AI extract and fill form data.  
🚀 **Foreign Key handling**: AI-assisted suggestions for ForeignKey fields.  
🚀 **Embedded AI chatbot**: A chatbot trained with your database schema to assist users and execute database queries on demand.  

---

## 🛠 Installation

### Prerequisites
- Python **3.8+**  
- Django **3.0+**  

### Install via pip

```bash
pip install django-admin-ai
```

---

## ⚙️ Setup

### 1️⃣ Add `django_admin_ai` to your Django settings

In your project's `settings.py`, update the following:

```python
import django_admin_ai
import os

INSTALLED_APPS = [
    ...,
    'django_admin_ai',  # Add this line
]

TEMPLATES = [
    {
        'DIRS': [
            os.path.join(BASE_DIR, 'templates/'),
            os.path.join(os.path.dirname(django_admin_ai.__file__), 'templates'),
        ],
    },
]
```

Define your OpenAI API key in `settings.py`:

```python
DJANGO_ADMIN_AI_CONFIG = {
    "openai_api_key": "<YOUR_OPENAI_API_KEY>"
}
```

---

### 2️⃣ Configure URL routing

In your project's `urls.py`, include Django Admin AI:

```python
from django.urls import path, include

urlpatterns = [
    path('admin-ai/', include('django_admin_ai.urls')),
]
```

---

### 3️⃣ Enable AI-powered forms in your models

In your Django **app’s `admin.py`**, simply add the `ai_import` flag to your admin models:

```python
from django.contrib import admin
from .models import YourModel

class YourModelAdmin(admin.ModelAdmin):
    ai_import = True  # Enable AI-driven form filling

admin.site.register(YourModel, YourModelAdmin)
```

Now, when you upload a **PDF, text file, or image**, the AI will extract relevant information and populate the fields automatically! 🎉

---

## 📜 License

This project is licensed under the **MIT License**. Feel free to contribute and improve the project!

---

## 💡 Contributing

We welcome contributions! If you’d like to add a feature or fix a bug, feel free to fork the repository and submit a pull request.

### 📬 Stay Updated
Follow the repository and stay tuned for updates!

---

🔥 Start enhancing your Django Admin with AI today! 🔥
