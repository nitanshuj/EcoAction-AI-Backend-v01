"""
Pytest configuration and shared fixtures
"""
import pytest
import os
from unittest.mock import Mock, patch


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment variables."""
    os.environ.update({
        "ENVIRONMENT": "test",
        "DEBUG": "True",
        "OPENAI_API_KEY": "test-openai-key",
        "SUPABASE_URL": "https://test.supabase.co",
        "SUPABASE_ANON_KEY": "test-anon-key",
        "SECRET_KEY": "test-secret-key"
    })


@pytest.fixture
def mock_supabase_client():
    """Mock Supabase client for testing."""
    with patch('data_model.supabase_client.init_supabase') as mock_init:
        mock_client = Mock()
        mock_init.return_value = mock_client
        yield mock_client


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "StrongP@ssw0rd1",
        "first_name": "John",
        "last_name": "Doe",
        "age": 25
    }


@pytest.fixture
def invalid_user_data():
    """Invalid user data for testing."""
    return {
        "email": "invalid-email",
        "password": "weak",
        "first_name": "J",
        "last_name": "",
        "age": 12
    }