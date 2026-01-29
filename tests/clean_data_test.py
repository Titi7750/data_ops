""" File containing unit tests for data cleaning functions in clean_data.py. """

import numpy as np
import pandas as pd
from src.clean_data import _fix_age

class TestFixAge:
    """ Tests for the _fix_age function. """

    def test_fix_age_basic(self):
        """ Test basic age cleaning without invalid values. """

        dataframe = pd.DataFrame({"age": [25, 30, 45]})
        result = _fix_age(dataframe)

        assert result["age"].tolist() == [25, 30, 45]

    def test_fix_age_with_invalid_values(self):
        """ Test age cleaning with invalid values replacement. """

        dataframe = pd.DataFrame({"age": [25, "invalid", 45, "unknown"]})
        result = _fix_age(dataframe, param_invalid_values=["invalid", "unknown"])

        assert result["age"].dtype == np.int64
        assert result["age"][1] == 16
        assert result["age"][3] == 16

    def test_fix_age_boundary_values(self):
        """ Test age boundaries (16-99). """

        dataframe = pd.DataFrame({"age": [15, 16, 99, 100, 150]})
        result = _fix_age(dataframe)

        assert result["age"][0] == 16
        assert result["age"][1] == 16
        assert result["age"][2] == 99
        assert result["age"][3] == 16
        assert result["age"][4] == 16

    def test_fix_age_with_na_values(self):
        """ Test age cleaning with NA/NaN values. """

        dataframe = pd.DataFrame({"age": [25, np.nan, 35, None]})
        result = _fix_age(dataframe)

        assert result["age"][1] == 16
        assert result["age"][3] == 16
