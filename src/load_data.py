""" Load customer data from raw CSV files. """

import os
import pandas as pd

# -----

def load_customers_data():
    """
    Load customer data from raw CSV files.

    Returns:
        tuple: Three dataframes containing customer data from the raw files
    """

    dataframe_customers_dirty = pd.read_csv(
        os.path.join(
            os.getcwd(),
            "data",
            "raw",
            "customers_dirty.csv"
        ),
        sep=","
    )

    dataframe_customers_dirty_2 = pd.read_csv(
        os.path.join(
            os.getcwd(),
            "data",
            "raw",
            "customers_dirty2.csv"
        ),
        sep=","
    )

    dataframe_customers_dirty_3 = pd.read_csv(
        os.path.join(
            os.getcwd(),
            "data",
            "raw",
            "customers_dirty3.csv"
        ),
        sep=","
    )

    return dataframe_customers_dirty, dataframe_customers_dirty_2, dataframe_customers_dirty_3
