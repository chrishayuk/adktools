"""Tests for the response models."""

from typing import Literal

import pytest
from pydantic import ValidationError

from adktools.models import DomainError, ErrorResponse, SuccessResponse


def test_success_response_model():
    """Test that SuccessResponse model works correctly."""
    # Test with simple result
    response = SuccessResponse(result="test")
    assert response.status == "success"
    assert response.result == "test"

    # Test with dict result
    response = SuccessResponse(result={"key": "value"})
    assert response.status == "success"
    assert response.result["key"] == "value"

    # Test serialization
    data = response.model_dump()
    assert data["status"] == "success"
    assert data["result"]["key"] == "value"


def test_error_response_model():
    """Test that ErrorResponse model works correctly."""
    response = ErrorResponse(error_message="An error occurred")
    assert response.status == "error"
    assert response.error_message == "An error occurred"

    # Test serialization
    data = response.model_dump()
    assert data["status"] == "error"
    assert data["error_message"] == "An error occurred"


def test_domain_error_inheritance():
    """Test that custom error models can inherit from DomainError."""

    class CustomError(DomainError):
        error_type: Literal["custom"] = "custom"
        param: str

    error = CustomError(param="test", message="Custom error")
    assert error.error_type == "custom"
    assert error.message == "Custom error"
    assert error.param == "test"


def test_domain_error_validation():
    """Test validation of domain error models."""

    class RequiredFieldsError(DomainError):
        error_type: Literal["required"] = "required"
        param: str

    # Missing required fields should raise ValidationError
    with pytest.raises(ValidationError):
        RequiredFieldsError(error_type="required")

    # This should work
    error = RequiredFieldsError(param="test", message="Required error")
    assert error.param == "test"
    assert error.message == "Required error"
