""" Tests for the _fix_country function in clean_data module."""

import pandas as pd
from src.clean_data import _fix_country

# -----

class TestFixCountry:
    """Tests for the _fix_country function."""

    def test_fix_country_default(self) -> None:
        """ Test default country standardization (uppercase). """

        dataframe = pd.DataFrame({"country": ["france", "usa", "Canada"]})
        result = _fix_country(dataframe)

        assert result["country"].tolist() == ["FRANCE", "USA", "CANADA"]

        return None

    # -----

    def test_fix_country_with_mappings(self) -> None:
        """ Test country fixing with custom mappings. """

        dataframe = pd.DataFrame({"country": ["France", "FRA", "USA"]})
        mappings = {"France": "FR", "FRA": "FR", "USA": "US"}
        result = _fix_country(dataframe, param_specific_mappings=mappings)

        assert result["country"][0] == "FR"
        assert result["country"][1] == "FR"
        assert result["country"][2] == "US"

        return None
