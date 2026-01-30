""" File for running the full data processing pipeline. """

from src.load_data import load_customers_data
from src.clean_data import clean_customers_data, save_cleaned_data

# -----

def run_pipeline():
    """ Run the data processing pipeline: load, clean, and save customer data. """

    df1, df2, df3 = load_customers_data()
    df1, df2, df3 = clean_customers_data(df1, df2, df3)
    save_cleaned_data(df1, df2, df3)

    return df1, df2, df3

# -----

if __name__ == "__main__":

    run_pipeline()
