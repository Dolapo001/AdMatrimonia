def get_serializer_error_as_string(errors) -> str:
    error_messages = []
    for field, error_list in errors.items():
        for error in error_list:
            field_label = field.replace("_", " ")
            error_messages.append(f"{field_label} input: {error}")
    return " | ".join(error_messages)
