""" Tests for the email cleaning functions. """

import pandas as pd
from src.clean_data import _fix_email

class TestFixEmail:
    """Tests for the _fix_email function."""

    def test_fix_email_default(self) -> None:
        """ Test default email fixing (add missing @). """

        dataframe = pd.DataFrame({"email": ["user@example.com", "userexample.com", "admin@domain.com"]})
        result = _fix_email(dataframe)

        assert "@" in result["email"][0]
        assert "@" in result["email"][1]
        assert "@" in result["email"][2]

        return None

    # -----

    def test_fix_email_format_name(self) -> None:
        """ Test email formatting with first.last@domain. """

        dataframe = pd.DataFrame({
            "email": ["john.doeexample.com", "jane.smithexample.com"],
            "full_name": ["John Doe", "Jane Smith"]
        })
        result = _fix_email(dataframe, param_specific_fix="format_name")

        assert "@" in result["email"][0]
        assert "example.com" in result["email"][0]

        assert "@" in result["email"][1]
        assert "example.com" in result["email"][1]

        return None

    # -----

    def test_fix_email_missing_domain(self) -> None:
        """ Test email with missing domain extension. """

        dataframe = pd.DataFrame({"email": ["user@example", "admin@example"]})
        result = _fix_email(dataframe, param_specific_fix="missing_domain")

        assert ".com" in result["email"][0]
        assert ".com" in result["email"][1]

        return None
