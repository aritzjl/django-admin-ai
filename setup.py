from setuptools import setup, find_packages

setup(
    name="django-admin-ai",  # Package name
    version="0.1.5",  # Update version as needed
    packages=find_packages(),  # Automatically find sub-packages
    include_package_data=True,  # Include static/templates
    install_requires=[
        "Django>=3.2",  # Define Django version requirement
        "openai>=1.61.0",  # AI functionality
        "annotated-types==0.7.0",
        "anyio==4.8.0",
        "asgiref==3.8.1",
        "build==1.2.2.post1",
        "certifi==2025.1.31",
        "colorama==0.4.6",
        "distro==1.9.0",
        "h11==0.14.0",
        "httpcore==1.0.7",
        "httpx==0.28.1",
        "idna==3.10",
        "jiter==0.8.2",
        "packaging==24.2",
        "pydantic==2.10.6",
        "pydantic_core==2.27.2",
        "pyproject_hooks==1.2.0",
        "setuptools==75.8.0",
        "sniffio==1.3.1",
        "sqlparse==0.5.3",
        "tqdm==4.67.1",
        "typing_extensions==4.12.2",
        "tzdata==2025.1",
        "PyPDF2>=2.10.1",
        "python-doctr==0.11.0",
        "Pillow>=8.0.0",
        "torch==2.6.0",
        "torchvision==0.21.0"
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
