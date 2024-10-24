import pandas as PD


def extract_from_excel(file_path):
    """
        Extracts and Clean Excel File
    """
    
    data_file = PD.read_excel(file_path)
    data_file_cleaned = data_file.dropna()
    data_file_cleaned = data_file_cleaned.drop_duplicates()
    return data_file_cleaned