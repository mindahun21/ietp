from django import template
import json

register = template.Library()

@register.filter
def get_json_field(instance, field_name):
    """
    Retrieve the JSON field value for a model instance.
    Returns an empty dictionary if the field does not exist or is None.
    """
    field_value = getattr(instance, field_name, {})
    try:
        if isinstance(field_value, str):
            return json.loads(field_value)  # Parse JSON if stored as string
        return field_value  # Already a dictionary
    except json.JSONDecodeError:
        return {}  # Return an empty dictionary on error
