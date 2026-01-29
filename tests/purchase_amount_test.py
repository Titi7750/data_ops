""" Tests for the _fix_purchase_amount function. """

import pandas as pd
from src.clean_data import _fix_purchase_amount

# -----

class TestFixPurchaseAmount:
    """ Tests for the _fix_purchase_amount function. """

    def test_fix_purchase_amount_positive(self) -> None:
        """ Test purchase amounts that are already positive. """

        dataframe = pd.DataFrame({"last_purchase_amount": [10.50, 25.00, 100.99]})
        result = _fix_purchase_amount(dataframe)

        assert result["last_purchase_amount"].tolist() == [10.50, 25.00, 100.99]

        return None

    # -----

    def test_fix_purchase_amount_negative(self) -> None:
        """ Test negative purchase amounts are set to 0. """

        dataframe = pd.DataFrame({"last_purchase_amount": [10.50, -5.00, -100.00, 0.0]})
        result = _fix_purchase_amount(dataframe)

        assert result["last_purchase_amount"][0] == 10.50
        assert result["last_purchase_amount"][1] == 0.0
        assert result["last_purchase_amount"][2] == 0.0
        assert result["last_purchase_amount"][3] == 0.0

        return None
