""" File containing unit tests for data cleaning functions in clean_data.py. """

import pandas as pd
from src.clean_data import _fix_signup_date

# -----

class TestFixSignupDate:
    """ Tests for the _fix_signup_date function. """

    def test_fix_signup_date_default(self) -> None:
        """ Test signup date cleaning with default replacement. """

        dataframe = pd.DataFrame({"signup_date": ["2024-01-15", "not_a_date", "2024-06-20"]})
        result = _fix_signup_date(dataframe)

        assert pd.notna(result["signup_date"][0])
        assert pd.notna(result["signup_date"][1])
        assert result["signup_date"].dtype == "datetime64[ns]"

        return None

    # -----

    def test_fix_signup_date_custom_replacements(self) -> None:
        """ Test signup date with custom replacements. """

        dataframe = pd.DataFrame({"signup_date": ["2024-01-15", "invalid_date", "2025-02-29"]})
        replacements = {"invalid_date": pd.NaT, "2025-02-29": "2025-02-28"}
        result = _fix_signup_date(dataframe, param_replacements=replacements)

        assert result["signup_date"].dtype == "datetime64[ns]"
        assert pd.notna(result["signup_date"][1])
        assert str(result["signup_date"][2].date()) == "2025-02-28"

        return None

    # -----

    def test_fix_signup_date_na_filling(self) -> None:
        """ Test that NaT values are filled with median. """

        dataframe = pd.DataFrame({"signup_date": ["2024-01-01", "2024-01-10", None]})
        result = _fix_signup_date(dataframe)

        assert pd.notna(result["signup_date"][2])

        return None
