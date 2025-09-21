"""
Improved authentication module with proper validation, error handling, and security.
"""
import logging
from typing import Tuple, Optional, Dict, Any
from supabase import Client
from .supabase_client import init_supabase
from .validators import UserValidator, DataSanitizer
from config.settings import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

class AuthError(Exception):
    """Custom authentication error."""
    pass

class AuthService:
    """Improved authentication service with proper validation and error handling."""

    def __init__(self):
        self.supabase: Client = init_supabase()
        self.validator = UserValidator()
        self.sanitizer = DataSanitizer()

    def sign_up(self, email: str, password: str, first_name: str, last_name: str, age: int) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Create a new user account with comprehensive validation.

        Args:
            email: User's email address
            password: User's password
            first_name: User's first name
            last_name: User's last name
            age: User's age

        Returns:
            Tuple of (success, message, user_data)
        """
        try:
            # Input sanitization
            email = self.sanitizer.sanitize_email(email)
            first_name = self.sanitizer.sanitize_name(first_name)
            last_name = self.sanitizer.sanitize_name(last_name)

            # Input validation
            email_valid, email_error = self.validator.validate_email_format(email)
            if not email_valid:
                return False, email_error, None

            password_valid, password_error = self.validator.validate_password_strength(password)
            if not password_valid:
                return False, password_error, None

            first_name_valid, first_name_error = self.validator.validate_name(first_name, "First name")
            if not first_name_valid:
                return False, first_name_error, None

            last_name_valid, last_name_error = self.validator.validate_name(last_name, "Last name")
            if not last_name_valid:
                return False, last_name_error, None

            age_valid, age_error = self.validator.validate_age(age)
            if not age_valid:
                return False, age_error, None

            # Attempt to create user
            logger.info(f"Attempting to create user with email: {email}")

            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            if not response.user:
                logger.warning(f"User creation failed for email: {email}")
                return False, "Account creation failed. Please try again.", None

            # Update user profile
            try:
                profile_response = self.supabase.table("users").update({
                    "first_name": first_name,
                    "last_name": last_name,
                    "age": age,
                    "onboarding_status": False,
                    "created_at": "now()"
                }).eq("id", response.user.id).execute()

                logger.info(f"User profile created successfully for: {email}")
                return True, "Account created successfully! Please check your email for verification.", {
                    "user_id": response.user.id,
                    "email": email
                }

            except Exception as db_error:
                logger.error(f"Profile update failed for {email}: {str(db_error)}")
                # User account was created but profile update failed
                return True, "Account created successfully, but some profile information may need to be updated later.", {
                    "user_id": response.user.id,
                    "email": email
                }

        except Exception as e:
            error_msg = str(e).lower()
            logger.error(f"Sign up error for {email}: {str(e)}")

            if "user already registered" in error_msg or "already been registered" in error_msg:
                return False, "An account with this email already exists. Please try signing in instead.", None
            elif "password" in error_msg and ("weak" in error_msg or "short" in error_msg):
                return False, "Password is too weak. Please choose a stronger password with at least 8 characters, including uppercase, lowercase, numbers, and special characters.", None
            elif "duplicate key" in error_msg:
                return False, "An account with this email already exists.", None
            elif "rate limit" in error_msg:
                return False, "Too many requests. Please wait a moment and try again.", None
            else:
                return False, "An unexpected error occurred during sign up. Please try again later.", None

    def sign_in(self, email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Authenticate user with email and password.

        Args:
            email: User's email address
            password: User's password

        Returns:
            Tuple of (success, message, user_data)
        """
        try:
            # Input sanitization and basic validation
            email = self.sanitizer.sanitize_email(email)

            if not email:
                return False, "Email is required.", None

            if not password:
                return False, "Password is required.", None

            logger.info(f"Attempting sign in for email: {email}")

            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            if not response.user:
                logger.warning(f"Sign in failed for email: {email}")
                return False, "Invalid email or password.", None

            logger.info(f"Sign in successful for email: {email}")
            return True, "Login successful!", {
                "user_id": response.user.id,
                "email": response.user.email,
                "last_sign_in": response.user.last_sign_in_at
            }

        except Exception as e:
            error_msg = str(e).lower()
            logger.error(f"Sign in error for {email}: {str(e)}")

            if "invalid login credentials" in error_msg or "invalid credentials" in error_msg:
                return False, "Invalid email or password.", None
            elif "email not confirmed" in error_msg:
                return False, "Please verify your email address before signing in.", None
            elif "rate limit" in error_msg:
                return False, "Too many login attempts. Please wait a moment and try again.", None
            else:
                return False, "An error occurred during login. Please try again later.", None

    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """
        Get the current authenticated user.

        Returns:
            User data if authenticated, None otherwise
        """
        try:
            response = self.supabase.auth.get_user()

            if response.user:
                return {
                    "id": response.user.id,
                    "email": response.user.email,
                    "created_at": response.user.created_at,
                    "last_sign_in_at": response.user.last_sign_in_at
                }

            return None

        except Exception as e:
            logger.error(f"Error getting current user: {str(e)}")
            return None

    def get_user_profile(self, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get user profile data from the users table.

        Args:
            user_id: User UUID, if not provided will use current user

        Returns:
            User profile data or None if not found
        """
        try:
            if not user_id:
                current_user = self.get_current_user()
                if not current_user:
                    return None
                user_id = current_user["id"]

            response = self.supabase.table("users").select("*").eq("id", user_id).execute()

            if response.data and len(response.data) > 0:
                return response.data[0]

            return None

        except Exception as e:
            logger.error(f"Error getting user profile for {user_id}: {str(e)}")
            return None

    def sign_out(self) -> Tuple[bool, str]:
        """
        Sign out the current user.

        Returns:
            Tuple of (success, message)
        """
        try:
            self.supabase.auth.sign_out()
            logger.info("User signed out successfully")
            return True, "Signed out successfully."
        except Exception as e:
            logger.error(f"Sign out error: {str(e)}")
            return False, "An error occurred during sign out."

    def reset_password(self, email: str) -> Tuple[bool, str]:
        """
        Send password reset email.

        Args:
            email: User's email address

        Returns:
            Tuple of (success, message)
        """
        try:
            email = self.sanitizer.sanitize_email(email)

            email_valid, email_error = self.validator.validate_email_format(email)
            if not email_valid:
                return False, email_error

            self.supabase.auth.reset_password_email(email)
            logger.info(f"Password reset email sent to: {email}")
            return True, "Password reset email sent. Please check your inbox."

        except Exception as e:
            logger.error(f"Password reset error for {email}: {str(e)}")
            return False, "An error occurred while sending the password reset email."

# Global auth service instance
auth_service = AuthService()

# Backward compatibility functions
def sign_up(email: str, password: str, first_name: str, last_name: str, age: int) -> Tuple[bool, str]:
    """Backward compatibility function."""
    success, message, _ = auth_service.sign_up(email, password, first_name, last_name, age)
    return success, message

def login(email: str, password: str) -> Tuple[bool, str]:
    """Backward compatibility function."""
    success, message, _ = auth_service.sign_in(email, password)
    return success, message

def get_current_user():
    """Backward compatibility function."""
    return auth_service.get_current_user()

def get_user_profile(user_id: str = None):
    """Backward compatibility function."""
    return auth_service.get_user_profile(user_id)

def logout():
    """Backward compatibility function."""
    success, _ = auth_service.sign_out()
    return success