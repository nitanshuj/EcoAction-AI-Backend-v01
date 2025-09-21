"""
Input validation utilities for the application.
"""
import re
from typing import Tuple, Optional
from email_validator import validate_email, EmailNotValidError

class ValidationError(Exception):
    """Custom validation error."""
    pass

class UserValidator:
    """Validates user input data."""

    @staticmethod
    def validate_email_format(email: str) -> Tuple[bool, str]:
        """
        Validate email format.

        Args:
            email: Email address to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            if not email or not email.strip():
                return False, "Email is required"

            # Use email-validator library for comprehensive validation
            validated_email = validate_email(email.strip())
            return True, ""
        except EmailNotValidError as e:
            return False, f"Invalid email format: {str(e)}"
        except Exception:
            return False, "Invalid email format"

    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, str]:
        """
        Validate password strength.

        Args:
            password: Password to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not password:
            return False, "Password is required"

        if len(password) < 8:
            return False, "Password must be at least 8 characters long"

        if len(password) > 128:
            return False, "Password must be less than 128 characters"

        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"

        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"

        # Check for at least one digit
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"

        # Check for at least one special character
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
            return False, "Password must contain at least one special character"

        return True, ""

    @staticmethod
    def validate_name(name: str, field_name: str = "Name") -> Tuple[bool, str]:
        """
        Validate name fields.

        Args:
            name: Name to validate
            field_name: Name of the field for error messages

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not name or not name.strip():
            return False, f"{field_name} is required"

        name = name.strip()

        if len(name) < 2:
            return False, f"{field_name} must be at least 2 characters long"

        if len(name) > 50:
            return False, f"{field_name} must be less than 50 characters long"

        # Allow letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            return False, f"{field_name} can only contain letters, spaces, hyphens, and apostrophes"

        return True, ""

    @staticmethod
    def validate_age(age: int) -> Tuple[bool, str]:
        """
        Validate age field.

        Args:
            age: Age to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if age is None:
            return False, "Age is required"

        try:
            age = int(age)
        except (ValueError, TypeError):
            return False, "Age must be a valid number"

        if age < 13:
            return False, "You must be at least 13 years old to use this service"

        if age > 120:
            return False, "Please enter a valid age"

        return True, ""

class DataSanitizer:
    """Sanitizes user input data."""

    @staticmethod
    def sanitize_string(value: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize string input.

        Args:
            value: String to sanitize
            max_length: Maximum allowed length

        Returns:
            Sanitized string
        """
        if not value:
            return ""

        # Strip whitespace
        sanitized = value.strip()

        # Remove null bytes
        sanitized = sanitized.replace('\x00', '')

        # Limit length if specified
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]

        return sanitized

    @staticmethod
    def sanitize_email(email: str) -> str:
        """Sanitize email input."""
        if not email:
            return ""
        return email.strip().lower()

    @staticmethod
    def sanitize_name(name: str) -> str:
        """Sanitize name input."""
        if not name:
            return ""

        # Strip and normalize whitespace
        sanitized = re.sub(r'\s+', ' ', name.strip())

        # Capitalize each word
        sanitized = ' '.join(word.capitalize() for word in sanitized.split())

        return sanitized