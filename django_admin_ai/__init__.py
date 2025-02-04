"""
Django Admin AI
---------------

An AI-powered enhancement for Django Admin that integrates artificial intelligence 
into the admin interface. This package provides utilities for AI-assisted data processing, 
automatic form population, intelligent suggestions, and more.

Key Features:
- Automated field population in Django models using AI

Author: [Aritz Jaber Lopes]
License: MIT
"""

__version__ = "0.1.0"
__author__ = "Aritz Jaber Lopes"
__license__ = "MIT"

# Import key components to make them accessible directly from the package
from .apps import DjangoAdminAIConfig
from .admin import AIAdminMixin
