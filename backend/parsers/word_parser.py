import docx

def extract_from_word(file_path):
    """
        Extracts Word Files
    """ 
    doc = docx.Document(file_path)
    
    paragraphs = [paragraph.text.strip() for paragraph in doc.paragraphs if paragraph.text.strip()]
    cleaned_paragraphs = list(dict.fromkeys(paragraphs))
    cleaned_paragraphs = "\n".join(cleaned_paragraphs)
    return cleaned_paragraphs
    