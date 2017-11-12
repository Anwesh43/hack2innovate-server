import pandas as pd
def get_currency():
    currency = list(set([c.lower() for c in pd.read_csv("country-code-to-currency-code-mapping.csv")['Code']]))
    currency.pop(currency.index("mad"))
    currency.append("rs")
    return currency
