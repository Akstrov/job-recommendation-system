import os

def get_project_root():
    """Returns project root folder."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_data_path(filename):
    """Returns path to a file in the data directory."""
    return os.path.join(get_project_root(), 'data', filename)

def get_models_path(filename):
    """Returns path to a file in the models directory."""
    return os.path.join(get_project_root(), 'models', filename)