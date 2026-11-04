from typing import Optional, Type
from django.apps import apps
from django.db import models

def get_model_from_string(
    model_app_label: str, 
    model_class_name: str
) -> Optional[Type[models.Model]]:
    """
    Get a Django model class
    
    Args:
        model_app_label: The Django app label
        model_class_name: The model class name
        
    Returns:
        The model class if found, None otherwise
        
    """
    # Input validation
    if not model_app_label or not model_class_name:
        raise ValueError("Both app label and model name must be provided")
    
    if not isinstance(model_app_label, str) or not isinstance(model_class_name, str):
        raise ValueError("App label and model name must be strings")
    
    # Clean inputs
    app_label = model_app_label.strip().lower()
    class_name = model_class_name.strip().lower()
    
    if not app_label or not class_name:
        raise ValueError("App label and model name cannot be empty after stripping")
    
    try:
        model_class = apps.get_model(app_label, class_name)
        return model_class
    except (ValueError, LookupError) as e:
        print(f"Failed to get model '{class_name}' from app '{app_label}': {e}")
        return None