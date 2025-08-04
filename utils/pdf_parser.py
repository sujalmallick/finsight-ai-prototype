from PyPDF2 import PdfReader

def extract_text_from_pdf(uploaded_pdf):
    # Create a PDF reader object using the uploaded file
    reader = PdfReader(uploaded_pdf)
    text = ""

    # Loop through each page and extract text
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:  # Make sure there's text (some pages may be images)
            text += extracted + "\n"

    return text
