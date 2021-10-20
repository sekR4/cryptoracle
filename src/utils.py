import requests
import datetime
import pandas as pd


def get_ts(
    coin: str = "nexo", vs_currency: str = "eur", days: int = 30
) -> pd.DataFrame:
    """Queries time series data from the coingecko API of a selected coin/token.
    The result will be returned in a pandas DataFrame.

    Parameters
    ----------
    coin : str, optional
        Coin or token e.g. "bitcoin", by default "nexo"
    vs_currency : str, optional
        Currency price is displayed in, by default "eur"
    days : int, optional
        Last x days, by default 30

    Returns
    -------
    pd.DataFrame
        example:
                    prices
        dates
        2021-08-22	1.609613
        2021-08-23	1.645399
        2021-08-24	1.671302
    """

    # https://www.coingecko.com/api/documentations/v3#/coins/get_coins__id__market_chart
    params = {
        "coin": coin,
        "vs_currency": vs_currency,
        "days": days,
        "interval": "daily",  # NOTE: To keep it simple, we'll focus on daily prices only
    }
    base_url = "https://api.coingecko.com/api/v3/coins/"
    param_url = (
        "{coin}/market_chart?vs_currency={vs_currency}&days={days}&interval={interval}"
    )
    url = base_url + param_url.format(**params)

    page = requests.get(url)

    if page.status_code == 200:
        prices = [i[1] for i in page.json()["prices"]]
        dates = [
            datetime.date.fromtimestamp(i[0] / 1000) for i in page.json()["prices"]
        ]

        df = pd.DataFrame({"dates": dates, "prices": prices})
        df.index = df.dates
        df.drop("dates", axis=1, inplace=True)

        return df
