from django.db import models

from skytek_utils.django.models import text_choices_max_length


def test_text_choices_max_length():
    class TestEnum(models.TextChoices):
        """Simple TextChoices implementation for testing"""

        ONE = "one", "One"
        THREE = "three", "Three"
        FOUR = "four", "Four"

    result = text_choices_max_length(TestEnum)

    assert result == len("three")
