import pytest

from pytest_django.lazy_django import skip_if_no_django
from rest_framework import test


@pytest.fixture
def api_client():
    """A DRF API test client instance.
    """
    skip_if_no_django()
    return test.APIClient()
