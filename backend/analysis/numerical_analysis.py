import pandas as PD

def analyze_numerical_data(data_file):
    """
    Analyze numerical data from a pandas DataFrame.
    Generates basic stats like sum, mean, and other aggregations.
    """
    analysis = {}
    
    for column in data_file.select_dtypes(include=["float64", "int64"]).columns:
            analysis[column] = {
            'sum': data_file[column].sum(),
            'mean': data_file[column].mean(),
            'min': data_file[column].min(),
            'max': data_file[column].max(),
            'std_dev': data_file[column].std()
        }
    return analysis