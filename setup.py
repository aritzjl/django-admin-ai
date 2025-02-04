from setuptools import setup, find_packages

setup(
    name="django-admin-ai",  # Package name
    version="0.1.2",  # Update version as needed
    packages=find_packages(),  # Automatically find sub-packages
    include_package_data=True,  # Include static/templates
    install_requires=[
        "Django>=3.2",  # Define Django version requirement
        "openai>=1.0",  # AI functionality
    ],
    python_requires=">=3.7",  # Define minimum Python version
    description="An AI-powered assistant for Django Admin, allowing data import using OpenAI.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Aritz Jaber Lopes",
    author_email="aritzzjl@gmail.com",
    url="https://github.com/aritzjl/django-admin-ai",  # Update with your GitHub
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
