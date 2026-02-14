def validate_admin(user) -> bool:
    """
    Validates if the user has admin privileges.

    Args:
        user (User): The user object to validate.
    Returns:
        bool: True if the user is an admin, False otherwise.
    """
    return user.role.name == "admin"