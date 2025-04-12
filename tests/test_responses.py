"""Tests for the response utility functions."""

from adktools.responses import error_response, success_response


def test_success_response_function():
    """Test the success_response utility function."""
    # Test with simple string
    response = success_response("test")
    assert response["status"] == "success"
    assert response["result"] == "test"

    # Test with dictionary
    response = success_response({"key": "value"})
    assert response["status"] == "success"
    assert response["result"]["key"] == "value"

    # Test with list
    response = success_response([1, 2, 3])
    assert response["status"] == "success"
    assert response["result"] == [1, 2, 3]

    # Test with complex nested structure
    complex_data = {
        "users": [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}],
        "metadata": {"total": 2, "page": 1},
    }
    response = success_response(complex_data)
    assert response["status"] == "success"
    assert response["result"]["users"][0]["name"] == "Alice"
    assert response["result"]["metadata"]["total"] == 2


def test_error_response_function():
    """Test the error_response utility function."""
    # Simple error message
    response = error_response("An error occurred")
    assert response["status"] == "error"
    assert response["error_message"] == "An error occurred"

    # Empty error message
    response = error_response("")
    assert response["status"] == "error"
    assert response["error_message"] == ""

    # Multi-line error message
    error_msg = "Multiple line\nerror message\nwith details"
    response = error_response(error_msg)
    assert response["status"] == "error"
    assert response["error_message"] == error_msg
