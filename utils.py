from PIL import Image
from pdf2image import convert_from_bytes
import google.generativeai as genai
import io
import zipfile
import os

# Load environment variables
# from dotenv import load_dotenv
# load_dotenv()

# Configure GenerativeAI service
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key="AIzaSyCdgSFHbBq22_yqNq-pZsGbITs57THy2Ps")
def get_gemini_response(image_data, input_prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_prompt, image_data])
    return response.text

# Function to prepare uploaded images for processing
def input_image_setup(file_bytes, file_type):
    # if file_type == "application/pdf":
    #     images = convert_from_bytes(file_bytes)
    #     image_parts = [{
    #         "mime_type": "image/jpeg",
    #         "data": images[0]._repr_png_()
    #     }]
    #     return image_parts, images
    #     else:
    image = Image.open(io.BytesIO(file_bytes))
    buffered = io.BytesIO()

    # Determine the format of the input image
    image_format = image.format.lower()

    # Save the image in the appropriate format
    if image_format in ['jpeg', 'jpg']:
        image.save(buffered, format="JPEG")
        mime_type = "image/jpeg"
    elif image_format == 'png':
        image.save(buffered, format="PNG")
        mime_type = "image/png"
    else:
        # Handle unsupported formats (optional)
        raise ValueError("Unsupported image format")

    # Prepare the image parts
    image_parts = [{
        "mime_type": mime_type,
        "data": buffered.getvalue()
    }]

    return image_parts, [image]

# Function to extract PDFs from a zip file
def extract_pdfs_from_zip(zip_file):
    pdf_files = []
    with zipfile.ZipFile(zip_file) as z:
        for file_name in z.namelist():
            if file_name.endswith('.pdf'):
                with z.open(file_name) as pdf_file:
                    pdf_files.append(pdf_file.read())
    return pdf_files

# Function to format the extracted response
def format_response(response_text, file_name):
    formatted_response = f"File: {file_name}\n\n"
    fields = response_text.split("\n")
    for field in fields:
        if ":" in field:
            field_name, value = field.split(":", 1)
            value = value.strip().replace("\\n", "\n")
            formatted_response += f"{field_name.strip()}:\n{value}\n\n"
    return formatted_response




