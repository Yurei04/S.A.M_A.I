import fitz

def extract_from_pdf(file_path):
    """
        Extract and Clean PDF
    """
    doc = fitz.open(file_path)
    text = ""
    
    for page in doc:
        text += page.get_text()
            
    doc.close()
    
    lines = text.splitlines()
    cleaned_lines = list(dict.fromkeys([lines.strip() for lines in lines if lines.strip()]))
    cleaned_text = "\n".join(cleaned_lines)
    return cleaned_text