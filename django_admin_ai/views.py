from django.http import JsonResponse
from django.apps import apps
from openai import OpenAI
import json


def get_form_structure(model):
    """
    Obtiene la estructura del formulario en base al modelo de Django.
    Devuelve un JSON con los nombres y tipos de los campos, excluyendo ForeignKeys.
    """
    fields_structure = {}
    for field in model._meta.fields:
        field_type = field.get_internal_type()

        # Excluir ForeignKey
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
            fields_structure[field.name] = field_type  # Solo incluimos campos editables

    return json.dumps(fields_structure)


def extract_data(form_fields, file_content):
    """
    Usa OpenAI GPT para extraer información del contenido del archivo `.txt` y mapearlo
    a los campos del formulario de Django.
    """
    api_key = open("key.txt").read().strip()  # Cargar clave desde un archivo seguro
    client = OpenAI(api_key=api_key)

    prompt = f"""
    You are a data extraction assistant. Your job is to extract structured data from the provided text.
    The data should be formatted as a JSON that correctly fills the Django form fields.
    
    Here is the extracted text from the file:
    ---
    {file_content}
    ---
    
    Here is the Django form structure:
    ---
    {form_fields}
    ---
    
    Return only a valid JSON with key-value pairs corresponding to the form fields. Make sure:
    - `BooleanField` values are `true` or `false`.
    - `DecimalField` values are formatted correctly (e.g., `1000.50`).
    - `IntegerField` values are whole numbers.
    - `DateField` values are in the format `YYYY-MM-DD`.
    """

    try:
        completion = client.chat.completions.create(
            response_format={ "type": "json_object" },
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are an intelligent assistant that extracts structured data from text. Respond in JSON format."},
                {"role": "user", "content": prompt}
            ]
        )

        response_text = completion.choices[0].message.content

        # Intentar parsear el JSON devuelto por la IA
        extracted_data = json.loads(response_text)
        print(extracted_data)
        return extracted_data

    except json.JSONDecodeError:
        print(f"Error al procesar la respuesta de la IA: {response_text}")
        return {"error": "Error al procesar la respuesta de la IA."}
    except Exception as e:
        return {"error": f"Error en la solicitud a OpenAI: {str(e)}"}


def ai_import_view(request, app_label, model_name):
    """
    Vista que recibe un archivo .txt, extrae datos con ChatGPT y devuelve un JSON
    con los valores estructurados para rellenar el formulario de Django.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido. Se requiere POST."}, status=405)

    # Obtener el archivo subido
    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No se ha subido ningún archivo."}, status=400)

    if not uploaded_file.name.endswith(".txt"):
        return JsonResponse({"error": "Solo se permiten archivos .txt."}, status=400)

    # Leer el contenido del archivo
    try:
        file_content = uploaded_file.read().decode("utf-8").strip()
    except UnicodeDecodeError:
        return JsonResponse({"error": "Error al leer el archivo. Asegúrate de que sea un .txt válido."}, status=400)

    # Obtener el modelo dinámicamente
    model = apps.get_model(app_label, model_name)
    if not model:
        return JsonResponse({"error": "Modelo no encontrado."}, status=400)

    # Obtener la estructura del formulario
    form_structure = get_form_structure(model)

    # Extraer datos usando IA
    extracted_data = extract_data(form_structure, file_content)

    return JsonResponse(extracted_data)
