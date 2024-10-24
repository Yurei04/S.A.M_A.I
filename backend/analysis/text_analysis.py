from transformers import pipeline

summarizer = pipeline("summarization")

def generate_summary(text, max_length=150, min_length=30):
    """
        Generates Summary Report
    """
    
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]["summary_text"]