"""
Tests for authentication module
"""
import pytest
from unittest.mock import Mock, patch
from data_model.validators import UserValidator, DataSanitizer
from data_model.auth_improved import AuthService


class TestUserValidator:
    """Test the UserValidator class."""

    def test_validate_email_format_valid(self):
        """Test valid email validation."""
        is_valid, error = UserValidator.validate_email_format("test@example.com")
        assert is_valid is True
        assert error == ""

    def test_validate_email_format_invalid(self):
        """Test invalid email validation."""
        is_valid, error = UserValidator.validate_email_format("invalid-email")
        assert is_valid is False
        assert "Invalid email format" in error

    def test_validate_email_format_empty(self):
        """Test empty email validation."""
        is_valid, error = UserValidator.validate_email_format("")
        assert is_valid is False
        assert "Email is required" in error

    def test_validate_password_strength_valid(self):
        """Test valid password validation."""
        is_valid, error = UserValidator.validate_password_strength("StrongP@ssw0rd1")
        assert is_valid is True
        assert error == ""

    def test_validate_password_strength_weak(self):
        """Test weak password validation."""
        is_valid, error = UserValidator.validate_password_strength("weak")
        assert is_valid is False
        assert "at least 8 characters" in error

    def test_validate_password_strength_no_uppercase(self):
        """Test password without uppercase."""
        is_valid, error = UserValidator.validate_password_strength("password123!")
        assert is_valid is False
        assert "uppercase letter" in error

    def test_validate_name_valid(self):
        """Test valid name validation."""
        is_valid, error = UserValidator.validate_name("John Doe", "First name")
        assert is_valid is True
        assert error == ""

    def test_validate_name_invalid_characters(self):
        """Test name with invalid characters."""
        is_valid, error = UserValidator.validate_name("John123", "First name")
        assert is_valid is False
        assert "can only contain letters" in error

    def test_validate_name_too_short(self):
        """Test name too short."""
        is_valid, error = UserValidator.validate_name("J", "First name")
        assert is_valid is False
        assert "at least 2 characters" in error

    def test_validate_age_valid(self):
        """Test valid age validation."""
        is_valid, error = UserValidator.validate_age(25)
        assert is_valid is True
        assert error == ""

    def test_validate_age_too_young(self):
        """Test age too young."""
        is_valid, error = UserValidator.validate_age(12)
        assert is_valid is False
        assert "at least 13 years old" in error

    def test_validate_age_invalid(self):
        """Test invalid age."""
        is_valid, error = UserValidator.validate_age("invalid")
        assert is_valid is False
        assert "valid number" in error


class TestDataSanitizer:
    """Test the DataSanitizer class."""

    def test_sanitize_string_basic(self):
        """Test basic string sanitization."""
        result = DataSanitizer.sanitize_string("  hello world  ")
        assert result == "hello world"

    def test_sanitize_string_with_null_bytes(self):
        """Test string sanitization with null bytes."""
        result = DataSanitizer.sanitize_string("hello\x00world")
        assert result == "helloworld"

    def test_sanitize_string_max_length(self):
        """Test string sanitization with max length."""
        result = DataSanitizer.sanitize_string("very long string", 5)
        assert result == "very "

    def test_sanitize_email(self):
        """Test email sanitization."""
        result = DataSanitizer.sanitize_email("  TEST@EXAMPLE.COM  ")
        assert result == "test@example.com"

    def test_sanitize_name(self):
        """Test name sanitization."""
        result = DataSanitizer.sanitize_name("john   doe")
        assert result == "John Doe"


class TestAuthService:
    """Test the AuthService class."""

    @pytest.fixture
    def auth_service(self):
        """Create a mock auth service for testing."""
        with patch('data_model.auth_improved.init_supabase') as mock_supabase:
            mock_client = Mock()
            mock_supabase.return_value = mock_client
            service = AuthService()
            service.supabase = mock_client
            return service

    def test_sign_up_valid_data(self, auth_service):
        """Test sign up with valid data."""
        # Mock successful supabase response
        mock_user = Mock()
        mock_user.id = "test-user-id"
        mock_response = Mock()
        mock_response.user = mock_user

        auth_service.supabase.auth.sign_up.return_value = mock_response
        auth_service.supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = Mock(data=[{}])

        success, message, user_data = auth_service.sign_up(
            "test@example.com",
            "StrongP@ssw0rd1",
            "John",
            "Doe",
            25
        )

        assert success is True
        assert "successfully" in message.lower()
        assert user_data is not None
        assert user_data["user_id"] == "test-user-id"

    def test_sign_up_invalid_email(self, auth_service):
        """Test sign up with invalid email."""
        success, message, user_data = auth_service.sign_up(
            "invalid-email",
            "StrongP@ssw0rd1",
            "John",
            "Doe",
            25
        )

        assert success is False
        assert "email format" in message.lower()
        assert user_data is None

    def test_sign_up_weak_password(self, auth_service):
        """Test sign up with weak password."""
        success, message, user_data = auth_service.sign_up(
            "test@example.com",
            "weak",
            "John",
            "Doe",
            25
        )

        assert success is False
        assert "password" in message.lower()
        assert user_data is None

    def test_sign_in_valid_credentials(self, auth_service):
        """Test sign in with valid credentials."""
        # Mock successful supabase response
        mock_user = Mock()
        mock_user.id = "test-user-id"
        mock_user.email = "test@example.com"
        mock_user.last_sign_in_at = "2023-01-01T00:00:00Z"
        mock_response = Mock()
        mock_response.user = mock_user

        auth_service.supabase.auth.sign_in_with_password.return_value = mock_response

        success, message, user_data = auth_service.sign_in(
            "test@example.com",
            "password123"
        )

        assert success is True
        assert "successful" in message.lower()
        assert user_data is not None
        assert user_data["user_id"] == "test-user-id"

    def test_sign_in_empty_email(self, auth_service):
        """Test sign in with empty email."""
        success, message, user_data = auth_service.sign_in("", "password123")

        assert success is False
        assert "email is required" in message.lower()
        assert user_data is None

    def test_sign_in_empty_password(self, auth_service):
        """Test sign in with empty password."""
        success, message, user_data = auth_service.sign_in("test@example.com", "")

        assert success is False
        assert "password is required" in message.lower()
        assert user_data is None


if __name__ == "__main__":
    pytest.main([__file__])