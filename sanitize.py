import html
import re

def sanitize_input(input_string):
    # Escape HTML entities
    sanitized_string = html.escape(input_string)
    
    # Remove script tags and content
    sanitized_string = re.sub(r'<script.*?>.*?</script>', '', sanitized_string, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove any remaining HTML tags
    sanitized_string = re.sub(r'<[^>]+>', '', sanitized_string)
    
    return sanitized_string

def sanitize_data(data):
    if isinstance(data, dict):
        return {key: sanitize_data(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_data(item) for item in data]
    elif isinstance(data, str):
        return sanitize_input(data)
    else:
        return data