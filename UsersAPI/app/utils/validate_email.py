def validate_email(email: str) -> bool:
    """
    Validates the format of an email address.

    Args:
        email (str): The email address to validate.
    Returns:
        bool: True if the email format is valid, False otherwise.
    """
    import re

    # Define a regex pattern for validating an email
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Use re.match to check if the email matches the pattern
    if re.match(email_pattern, email):
        return True
    else:
        return False