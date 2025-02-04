import json
from django.http import JsonResponse
from django.apps import apps
from django.conf import settings
from openai import OpenAI

# Load configuration from Django settings
DJANGO_ADMIN_AI_CONFIG = settings.DJANGO_ADMIN_AI_CONFIG
OPENAI_API_KEY = DJANGO_ADMIN_AI_CONFIG.get("openai_api_key")


def get_form_structure(model):
    """
    Retrieves the structure of a Django model form.
    Returns a JSON object containing field names and their types, excluding ForeignKeys.
    """
    if not model:
        raise ValueError("Invalid model provided.")

    fields_structure = {}

    for field in model._meta.fields:
        field_type = field.get_internal_type()

        # Exclude ForeignKey fields
        if field_type == "ForeignKey":
            continue

        if field_type in [
            "CharField",
            "TextField",
            "IntegerField",
            "FloatField",
            "DecimalField",
            "BooleanField",
            "DateField",
            "DateTimeField",
        ]:
            fields_structure[field.name] = field_type  # Include only editable fields

    return json.dumps(fields_structure)


def extract_data(form_fields, file_content):
    """
    Uses OpenAI GPT to extract structured data from a `.txt` file content
    and map it to Django form fields.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OpenAI API key is missing in settings.")

    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"""
    You are a data extraction assistant. Your job is to extract structured data from the provided text.
    The data should be formatted as JSON that correctly matches the Django form fields.

    Extracted text from the file:
    ---
    {file_content}
    ---

    Django form structure:
    ---
    {form_fields}
    ---

    Return only a valid JSON with key-value pairs corresponding to the form fields. Ensure:
    - `BooleanField` values are `true` or `false`.
    - `DecimalField` values are properly formatted (e.g., `1000.50`).
    - `IntegerField` values are whole numbers.
    - `DateField` values follow the `YYYY-MM-DD` format.
    """

    try:
        completion = client.chat.completions.create(
            response_format={"type": "json_object"},
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are an intelligent assistant that extracts structured data from text. Respond in JSON format."},
                {"role": "user", "content": prompt},
            ],
        )

        response_text = completion.choices[0].message.content

        # Parse the JSON response from the AI
        extracted_data = json.loads(response_text)
        return extracted_data

    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse AI response as JSON: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"OpenAI request error: {str(e)}")


def ai_import_view(request, app_label, model_name):
    """
    Django view to handle a `.txt` file upload, extract data using OpenAI, 
    and return structured JSON data for form auto-filling.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed. Use POST."}, status=405)

    # Retrieve the uploaded file
    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No file uploaded."}, status=400)

    if not uploaded_file.name.endswith(".txt"):
        return JsonResponse({"error": "Only .txt files are allowed."}, status=400)

    # Read file content
    try:
        file_content = uploaded_file.read().decode("utf-8").strip()
    except UnicodeDecodeError:
        return JsonResponse({"error": "Invalid file format. Ensure it is a valid .txt file."}, status=400)

    # Dynamically retrieve the Django model
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError:
        return JsonResponse({"error": "Model not found."}, status=400)

    # Generate form structure JSON
    form_structure = get_form_structure(model)

    # Extract structured data using AI
    try:
        extracted_data = extract_data(form_structure, file_content)
    except (ValueError, RuntimeError) as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse(extracted_data)
