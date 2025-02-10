import json
from django.http import JsonResponse
from django.apps import apps
from django.conf import settings
from openai import OpenAI
import PyPDF2
from doctr.models import ocr_predictor
from doctr.io import DocumentFile
import os
from openai import OpenAI

# Load configuration from Django settings
DJANGO_ADMIN_AI_CONFIG = settings.DJANGO_ADMIN_AI_CONFIG
OPENAI_API_KEY = DJANGO_ADMIN_AI_CONFIG.get("openai_api_key")

model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)

def extract_text_from_audio(uploaded_audio):
    """
    Extracts text from an uploaded audio file (e.g., MP3, WAV) using OpenAI's Whisper model.
    Returns the transcribed text as a string.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    try:
        # Save the uploaded file temporarily to disk with the appropriate extension
        audio_extension = uploaded_audio.name.split('.')[-1].lower()
        temp_audio_filename = f"temp_audio.{audio_extension}"

        # Save the audio file to disk
        with open(temp_audio_filename, "wb") as f:
            for chunk in uploaded_audio.chunks():
                f.write(chunk)

        # Open the audio file to send it to the OpenAI API
        with open(temp_audio_filename, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",  # Whisper model
                file=audio_file,
                response_format="text"  # To get plain text response
                
            )
        return transcription

    except Exception as e:
        raise ValueError(f"Error processing the audio: {str(e)}")

def extract_text_from_image(uploaded_file):
    """
    Extracts text from an uploaded image file (any format: PNG, JPEG, JPG, BMP, etc.) using OCR.
    Returns the extracted text as a string.
    """
    try:
        # Save the uploaded file temporarily to disk with the appropriate extension
        # Get file extension to ensure it's saved correctly
        file_extension = uploaded_file.name.split('.')[-1].lower()
        temp_filename = f"temp_image.{file_extension}"

        with open(temp_filename, "wb") as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        # Initialize the OCR model
        model = ocr_predictor(pretrained=True)
        
        # Load the image and extract text
        single_img_doc = DocumentFile.from_images(temp_filename)
        result = model(single_img_doc)

        # Log before deleting the temporary file

        # Delete the temporary image file after processing
        os.remove(temp_filename)

        # Log the result for debugging
        return result

    except Exception as e:
        raise ValueError(f"Error processing the image: {str(e)}")
    
def extract_text_from_pdf(uploaded_file):
    """
    Extract text from a PDF file using PyPDF2.
    Returns the extracted text as a string.
    """
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() or ""
        return text.strip()
    except Exception as e:
        raise ValueError(f"Error reading PDF file: {str(e)}")

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
    Django view to handle a `.txt`, `.pdf`, or `.png` file upload, extract data using OpenAI, 
    and return structured JSON data for form auto-filling.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed. Use POST."}, status=405)

    # Retrieve the uploaded file
    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No file uploaded."}, status=400)

    # Read file content
    try:
        if uploaded_file.name.endswith(".txt"):
            file_content = uploaded_file.read().decode("utf-8").strip()
        elif uploaded_file.name.endswith(".pdf"):
            file_content = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp")):
            file_content = extract_text_from_image(uploaded_file)
        elif uploaded_file.name.lower().endswith((".wav", ".m4a")):
            uploaded_audio = uploaded_file
            file_content = extract_text_from_audio(uploaded_audio)
        else:
            raise ValueError("Unsupported file type")
    except UnicodeDecodeError as e:
        return JsonResponse({"error": "Invalid file format. Ensure it is a valid .txt or .pdf file."}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Error processing the file: {str(e)}"}, status=500)

    # Dynamically retrieve the Django model
    try:
        model = apps.get_model(app_label, model_name)
    except LookupError as e:
        return JsonResponse({"error": "Model not found."}, status=400)

    # Generate form structure JSON
    form_structure = get_form_structure(model)

    # Extract structured data using AI
    try:
        extracted_data = extract_data(form_structure, file_content)
    except (ValueError, RuntimeError) as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse(extracted_data)
